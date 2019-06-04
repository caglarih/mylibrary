import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from book.models import Author, Book, Publisher
from book import tasks

from functions.product_query import (
    get_product_details,
    ProductQueryParameters,
)


@method_decorator(csrf_exempt, "dispatch")
class ExploreBookView(View):
    """Create book with given isbn number."""

    def post(self, request):
        """Fetch book data and create records."""

        body = json.loads(request.body)
        isbn = body.get("isbn")
        if isbn is None:
            return HttpResponse(status=400)
        details = get_product_details(ProductQueryParameters(isbn, None))
        author, _ = Author.objects.get_or_create(name=details["author"])
        publisher, _ = Publisher.objects.get_or_create(
            name=details["publisher"],
        )
        book = Book.objects.create(
            isbn=details["isbn"],
            name=details["name"],
            author=author,
            publisher=publisher,
            page_count=details["page_count"],
        )
        tasks.update_product_prices.delay(book.pk)
        return HttpResponse(json.dumps(details), status=201)
