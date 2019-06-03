import datetime

from celery import shared_task

from book.models import Book, BookPrice

from functions.comparison import engine
from functions.product_query import ProductQueryParameters



@shared_task
def update_product_prices(book_id):
    book = Book.objects.get(id=book_id)
    prices = engine.query_product(book.isbn)
    price_orms = {
        bp.supplier: bp
        for bp in BookPrice.objects.filter(book=book)
    }
    for supplier, price in prices.items():
        if supplier in price_orms:
            price_orm = price_orms[supplier]
            if price == price_orm.price:
                continue
            price_orm.price = price
            price_orm.history.append((datetime.date.today(), price))
            price_orm.save()
        else:
            BookPrice.objects.create(
                book=book,
                supplier=supplier,
                price=price,
            )
