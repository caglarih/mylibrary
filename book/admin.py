from django.contrib import admin

from book.constants import Shelf
from book.models import Author, Book, BookPrice, Publisher, ShelfEntry


class BookInlineAdmin(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInlineAdmin,
    ]


def track_prices(model_admin, request, queryset):
    ShelfEntry.objects.filter(
        book_id__in=queryset.values_list("pk", flat=True),
        shelf=Shelf.TOTRACK,
    ).delete()
    entries = [ShelfEntry(book=book, shelf=Shelf.TOTRACK)for book in queryset]
    ShelfEntry.objects.bulk_create(entries)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "publisher", "isbn", "page_count")
    list_select_related = ("author", "publisher")
    actions = (track_prices, )


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
            .prefetch_related("book__shelfentry_set") \
            .filter(book__shelfentry__shelf=Shelf.TOTRACK) \
            .order_by("book__name", "price") \
            .distinct("book__name")

    def get_book_name(self, obj):
        return obj.book.name


@admin.register(ShelfEntry)
class ShelfEntryAdmin(admin.ModelAdmin):
    list_display = ("book", "shelf")
    list_select_related = ("book", )
    list_filter = ("shelf", )
