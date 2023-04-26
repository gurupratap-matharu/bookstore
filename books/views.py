from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Book


class BookListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"
    paginate_by = 9


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"


class SearchResultsListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query)
        )
