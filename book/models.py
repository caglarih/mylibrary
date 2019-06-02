from django.db import models


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
