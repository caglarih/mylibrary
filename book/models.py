from django.contrib.postgres.fields import JSONField
from django.db import models

from book.constants import Shelf
from utils.book_suppliers import Supplier


__all__ = [
    "Author",
    "Book",
    "BookPrice",
    "Publisher",
]


SUPPLIER_CHOICES = [(s.value, s) for s in Supplier]
SHELF_CHOICES = [(s.value, s) for s in Shelf]


class AbstractTimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(AbstractTimestampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Publisher(AbstractTimestampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(AbstractTimestampedModel):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, primary_key=True, editable=False)
    page_count = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class BookPrice(AbstractTimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    supplier = models.SmallIntegerField(choices=SUPPLIER_CHOICES)
    price = models.PositiveIntegerField()
    history = JSONField(default=list)

    class Meta:
        unique_together = [
            ['book', 'supplier'],
        ]


class ShelfEntry(AbstractTimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf = models.SmallIntegerField(choices=SHELF_CHOICES, db_index=True)

    def __str__(self):
        return "%s - %s" % (self.book, Shelf(self.shelf).name)
