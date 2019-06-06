from django.contrib import admin

from book.models import Author, Book, BookPrice, Publisher


class BookInlineAdmin(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInlineAdmin,
    ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "publisher", "isbn", "page_count")
    list_select_related = ("author", "publisher")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    inlines = [
        BookInlineAdmin,
    ]


@admin.register(BookPrice)
class BookPriceAdmin(admin.ModelAdmin):
    list_display = ("get_book_name", "supplier", "price")
    list_select_related = ("book", )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset \
            .order_by("book__name", "price") \
            .distinct("book__name")

    def get_book_name(self, obj):
        return obj.book.name
