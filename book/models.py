from django.contrib.postgres.fields import JSONField
from django.db import models

from utils.book_suppliers import Supplier


SUPPLIER_CHOICES = [(s, s.value) for s in Supplier]


class AbstractTimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(AbstractTimestampedModel):
    name = models.CharField(max_length=50)


class Publisher(AbstractTimestampedModel):
    name = models.CharField(max_length=50)


class Book(AbstractTimestampedModel):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, primary_key=True, editable=False)
    page_count = models.PositiveSmallIntegerField()


class BookPrice(AbstractTimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    supplier = models.CharField(max_length=50, choices=SUPPLIER_CHOICES)
    price = models.PositiveIntegerField()
    history = JSONField(default=list)
