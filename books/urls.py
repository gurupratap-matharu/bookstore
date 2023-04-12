from django.urls import path

from .views import BookDetailView, BookListView, SearchResultsListView

app_name = "books"


urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<uuid:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
]
