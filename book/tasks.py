from datetime import datetime

from celery import shared_task

from book.models import Book, BookPrice, ShelfEntry

from functions.comparison import engine
from functions.product_query import ProductQueryParameters


__all__ = [
    "update_all_book_prices",
    "update_book_prices",
    "update_to_track_shelf_prices",
]


@shared_task
def update_all_book_prices():
    for book_pk in Book.objects.values_list("pk", flat=True):
        update_book_prices.delay(book_pk)


@shared_task
def update_book_prices(book_pk):
    """Update price data of given book.

    :param book_pk: Primary key of the Book record
    :type book_pk: str
    """
    book = Book.objects.get(pk=book_pk)
    prices = engine.query_product(book_pk, book.name)
    price_orms = {
        bp.supplier: bp
        for bp in BookPrice.objects.filter(book_id=book_pk)
    }
    today = datetime.now().strftime("%Y%m%d")
    for supplier, price in prices.items():
        if supplier in price_orms:
            price_orm = price_orms[supplier]
            if price == price_orm.price:
                continue
            price_orm.price = price
            price_orm.history.append((today, price))
            price_orm.save()
        else:
            BookPrice.objects.create(
                book_id=book_pk,
                supplier=supplier,
                price=price,
                history=[(today, price)],
            )


@shared_task
def update_to_track_shelf_prices():
    for book_pk in ShelfEntry.objects.values_list("book_id", flat=True):
        update_book_prices.delay(book_pk)
