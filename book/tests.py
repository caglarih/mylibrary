import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from book import models

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

    def _validate_created_records(self):
        book = models.Book.objects.first()
        self.assertEqual(book.author.name, self.details.author)
        self.assertEqual(book.publisher.name, self.details.publisher)
        self.assertEqual(book.isbn, self.details.isbn)
        self.assertEqual(book.page_count, self.details.page_count)
        self.assertEqual(book.name, self.details.name)

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
