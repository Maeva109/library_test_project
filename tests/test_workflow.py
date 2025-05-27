from django.test import Client
from django.contrib.auth.models import User
from library.models import Book, Author, BorrowRecord, Member
import pytest

@pytest.mark.django_db
class TestLibraryWorkflows:
    def test_book_add_to_borrow(self, client, admin_user):
        # 1. Créer un auteur
        author = Author.objects.create(first_name="Test", last_name="Author")

        # 2. Ajouter un livre (admin)
        client.force_login(admin_user)
        client.post('/admin/library/book/add/', {
            'title': 'New Book',
            'author': author.id,
            'isbn': '1234567890123',
            'quantity': 3,
            'available': 3,
            'category': 'FICTION',
            'publication_date': '2024-01-01'
        })
        book = Book.objects.get(title='New Book')

        # 3. Créer un membre et l'utilisateur associé
        user = User.objects.create_user(username='member', password='testpass')
        member = Member.objects.create(user=user)

        # 4. Le membre emprunte le livre
        member_client = Client()
        member_client.login(username='member', password='testpass')
        response = member_client.post(f'/library/books/{book.pk}/borrow/', {
            'book': book.pk,
            'member': member.pk,
            'due_date': '2024-12-31'
        })

        # 5. Vérifier
        assert response.status_code in (200, 302)
        assert BorrowRecord.objects.count() == 1
        assert Book.objects.get(pk=book.pk).available == 2