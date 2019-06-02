from django.contrib.postgres.fields import JSONField
from django.db import models

from utils.book_suppliers import Supplier


class Author(models.Model):
    name = models.CharField(max_length=50)


class Publisher(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.PositiveSmallIntegerField()


class BookPrice(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    supplier = models.CharField(
        max_length=50,
        choices=[(s, s.value) for s in Supplier],
    )
    price = models.PositiveIntegerField()
    history = JSONField(default=list)
