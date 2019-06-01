from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    page_count = models.PositiveSmallIntegerField()
