import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from library.models import Book, Author

@pytest.mark.django_db
class TestBookAPI:
    def test_list_books(self, book):
        client = APIClient()
        url = reverse('library:book-list')  # Using router-generated URL name
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == book.title

    def test_create_book(self, author):
        client = APIClient()
        url = reverse('library:book-list')  # Using router-generated URL name
        data = {
            'title': 'API Test Book',
            'author': author.id,
            'isbn': '9876543210987',
            'publication_date': '2023-01-01',
            'quantity': 3,
            'available': 3
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 201
        assert Book.objects.count() == 1

    