from django.urls import include, path

from book.views import ExploreBookView


urlpatterns = [
    path("explore/", ExploreBookView.as_view(), name="explore"),
]
