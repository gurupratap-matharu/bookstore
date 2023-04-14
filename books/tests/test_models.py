from django.test import TestCase

from books.factories import BookFactory
from books.models import Book


class BookModelTests(TestCase):
    """
    Test case for the book model.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.book = BookFactory()

    def test_str_representation(self):
        self.assertEqual(str(self.book), f"{self.book.title}")

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.book._meta.verbose_name_plural), "books")

    def test_book_creation_is_correct(self):
        book_from_db = Book.objects.first()

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(book_from_db.title, self.book.title)
        self.assertEqual(book_from_db.author, self.book.author)
        self.assertEqual(book_from_db.price, self.book.price)
        self.assertEqual(book_from_db.description, self.book.description)
        self.assertEqual(book_from_db.link, self.book.link)

    def test_book_name_max_length(self):
        book = Book.objects.first()
        max_length = book._meta.get_field("title").max_length  # type:ignore

        self.assertEqual(max_length, 200)

    def test_books_are_ordered_by_created_date(self):
        Book.objects.all().delete()

        b_1 = BookFactory(title="Book 1")
        b_2 = BookFactory(title="Book 2")
        b_3 = BookFactory(title="Book 3")

        books = Book.objects.all()

        self.assertEqual(books[0], b_3)
        self.assertEqual(books[1], b_2)
        self.assertEqual(books[2], b_1)

        ordering = books[0]._meta.ordering[0]

        self.assertEqual(ordering, "-created_on")
