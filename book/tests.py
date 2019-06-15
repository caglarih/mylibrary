import json
from unittest.mock import patch

import freezegun
from django.test import TestCase
from django.urls import reverse

from book.constants import Shelf
from book import models, tasks
from utils.book_suppliers import Supplier

from functions.product_query import (
    BookDetails,
    ProductQueryParameters,
)


class ExploreBookViewTestCase(TestCase):

    def setUp(self):
        self.details = BookDetails(
            isbn="ISBN",
            cover="COVER",
            size="NORMAL",
            page_count=100,
            name="BOOKNAME",
            author="AUTHOR",
            publisher="PUBLISHER",
        )
        self.parameters = ProductQueryParameters(self.details.isbn, None)
        self.url = reverse("book:explore")
        super().setUp()

    def test_post_without_isbn(self):
        response = self._post({})
        self.assertEqual(response.status_code, 400)

    @patch("book.tasks.update_book_prices")
    @patch("functions.product_query.get_product_details")
    def test_post_success(self, detail_getter_mock, price_updater_mock):
        detail_getter_mock.return_value = self.details
        response = self._post()
        self.assertEqual(response.status_code, 201)
        self._validate_record_counts()
        self._validate_created_records()
        self._validate_book_detail_getter_call(detail_getter_mock)
        self._validate_price_update_task_call(price_updater_mock)

    def _validate_record_counts(self):
        self.assertEqual(models.Author.objects.count(), 1)
        self.assertEqual(models.Publisher.objects.count(), 1)
        self.assertEqual(models.Book.objects.count(), 1)
        self.assertEqual(models.ShelfEntry.objects.count(), 1)

    def _validate_created_records(self):
        book = models.Book.objects.first()
        shelf_entry = book.shelfentry_set.first()
        self.assertEqual(book.author.name, self.details.author)
        self.assertEqual(book.publisher.name, self.details.publisher)
        self.assertEqual(book.isbn, self.details.isbn)
        self.assertEqual(book.page_count, self.details.page_count)
        self.assertEqual(book.name, self.details.name)
        self.assertEqual(shelf_entry.book, book)
        self.assertEqual(shelf_entry.shelf, Shelf.TOTRACK)

    def _validate_price_update_task_call(self, price_updater_mock):
        price_updater_mock.delay.assert_called_once_with(self.details.isbn)

    def _validate_book_detail_getter_call(self, detail_getter_mock):
        detail_getter_mock.assert_called_once_with(self.parameters)

    def _post(self, data=None):
        data = data if data is not None else {"isbn": self.details.isbn}
        return self.client.post(
            self.url,
            json.dumps(data),
            content_type="application/json",
        )


@freezegun.freeze_time("2019-02-02")
class BookPriceUpdateTestCase(TestCase):

    fixtures = [
        "author",
        "book",
        "bookprice",
        "publisher",
    ]

    def setUp(self):
        self.supplier = Supplier.KIDEGA
        self.book_price = models.BookPrice.objects.first()
        self.price = self.book_price.price
        self.book = models.Book.objects.first()
        self.updated_price = self.book_price.price * 2
        self.today = "20190202"
        self.updated_history = self.book_price.history + [
            [self.today, self.updated_price],
        ]
        super().setUp()

    @patch("functions.comparison.engine.query_product")
    def test_without_initial(self, query_product_mock):
        models.BookPrice.objects.all().delete()
        self._mock_query_product_response(query_product_mock)
        tasks.update_book_prices(self.book.pk)
        self._validate_query_product_call(query_product_mock)
        self._validate_single_book_price_record(
            self.price,
            [[self.today, self.price]],
        )

    @patch("functions.comparison.engine.query_product")
    def test_with_initial_same_price(self, query_product_mock):
        self._mock_query_product_response(query_product_mock)
        tasks.update_book_prices(self.book.pk)
        self._validate_query_product_call(query_product_mock)
        self._validate_single_book_price_record(
            self.price,
            self.book_price.history,
        )

    @patch("functions.comparison.engine.query_product")
    def test_with_initial_different_price(self, query_product_mock):
        self._mock_query_product_response(
            query_product_mock,
            self.updated_price,
        )
        tasks.update_book_prices(self.book.pk)
        self._validate_query_product_call(query_product_mock)
        self._validate_single_book_price_record(
            self.updated_price,
            self.updated_history,
        )

    def _mock_query_product_response(self, query_product_mock, price=None):
        query_product_mock.return_value = {
            self.supplier: price or self.price,
        }

    def _validate_single_book_price_record(self, price, history):
        self.assertEqual(models.BookPrice.objects.count(), 1)
        book_price = models.BookPrice.objects.first()
        self.assertEqual(book_price.book, self.book)
        self.assertEqual(book_price.price, price)
        self.assertEqual(book_price.supplier, self.supplier)
        self.assertEqual(book_price.history, history)

    def _validate_query_product_call(self, query_product_mock):
        query_product_mock.assert_called_once_with(self.book.pk, self.book.name)
