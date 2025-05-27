from django.urls import reverse
from django.test import TestCase, Client
from library.models import Book, Author, Member

class TestBookViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name="Test", last_name="Author")
        cls.book = Book.objects.create(
            title="Test Book",
            author=cls.author,
            isbn="1234567890123",
            publication_date="2023-01-01",
            quantity=5,
            available=5,
            category="FICTION"
        )
        cls.client = Client()

    def test_book_list_view(self):
        url = reverse('library:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_book_search_view(self):
        url = reverse('library:book-search') + '?q=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)