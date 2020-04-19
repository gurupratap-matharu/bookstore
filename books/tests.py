from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Book, Review


class BookTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='reviewuser',
            email='reviewuser@email.com',
            password='testpass123',
        )
        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00',
        )
        self.review1 = Review.objects.create(
            review='Loved the book!',
            author=self.user,
            book=self.book,
        )
        self.review2 = Review.objects.create(
            review='Amazing. Highly recommended!',
            author=self.user,
            book=self.book,
        )

    def test_book_is_properly_created(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertContains(response, 'Harry Potter')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'Loved the book!')
        self.assertContains(response, 'Highly recommended')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_review_is_properly_created(self):
        self.assertEqual(self.book.reviews.count(), 2)
        reviews = self.book.reviews.all()
        self.assertEqual(reviews[0].review, 'Loved the book!')
        self.assertEqual(reviews[1].review, 'Amazing. Highly recommended!')
