import pytest
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestBookAPI:
    def test_api_crud(self, author):
        client = APIClient()
        
        # CREATE
        response = client.post('/api/books/', {
            'title': 'API Book',
            'author': author.id,
            'isbn': '1234567890123',
            'category': 'FICTION',
            'quantity': 2,
            'available': 2,
            'publication_date': '2024-01-01'
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        book_id = response.data['id']
        
        # READ
        response = client.get('/api/books/')
        assert response.status_code == status.HTTP_200_OK
        assert any(book['id'] == book_id for book in response.data)
        
        # UPDATE
        response = client.patch(f'/api/books/{book_id}/', {
            'title': 'Updated Title'
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # DELETE
        response = client.delete(f'/api/books/{book_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT