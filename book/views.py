import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from book.constants import Shelf
from book.models import Author, Book, Publisher, ShelfEntry
from book import tasks

from functions import product_query


@method_decorator(csrf_exempt, "dispatch")
class ExploreBookView(View):
    """Create book with given isbn number."""

    @staticmethod
    def post(request):
        """Fetch book data and create records.

        :param request: Http request
        :type request: django.http.HttpRequest
        :rtype: django.http.HttpResponse
        """
        body = json.loads(request.body)
        isbn = body.get("isbn")
        if isbn is None:
            return HttpResponse(status=400)
        details = product_query.get_product_details(
            product_query.ProductQueryParameters(isbn),
        )
        author, _ = Author.objects.get_or_create(name=details.author)
        publisher, _ = Publisher.objects.get_or_create(name=details.publisher)
        book = Book.objects.create(
            isbn=details.isbn,
            name=details.name,
            author=author,
            publisher=publisher,
            page_count=details.page_count,
        )
        ShelfEntry.objects.create(book=book, shelf=Shelf.TOREAD)
        tasks.update_book_prices.delay(book.pk)
        return HttpResponse(json.dumps(details.__dict__), status=201)
