import pytest
from django.core.exceptions import ValidationError
from library.forms import BookForm, BorrowForm

@pytest.mark.django_db
class TestBookForm:
    def test_valid_form(self, author):
        form_data = {
            'title': 'New Book',
            'author': author.id,
            'isbn': '1234567890123',
            'publication_date': '2023-01-01',
            'quantity': 5,
            'available': 5
        }
        form = BookForm(data=form_data)
        assert form.is_valid()

    def test_invalid_isbn(self, author):
        form_data = {
            'title': 'New Book',
            'author': author.id,
            'isbn': 'invalidisbn',
            'publication_date': '2023-01-01',
            'quantity': 5
        }
        form = BookForm(data=form_data)
        assert not form.is_valid()
        assert 'isbn' in form.errors

@pytest.mark.django_db
class TestBorrowForm:
    def test_borrow_available_book(self, book, member):
        form_data = {
            'book': book.id,
            'member': member.id,
            'due_date': '2023-12-31'
        }
        form = BorrowForm(data=form_data)
        assert form.is_valid()

    def test_borrow_unavailable_book(self, unavailable_book, member):
        form_data = {
            'book': unavailable_book.id,
            'member': member.id,
            'due_date': '2023-12-31'
        }
        form = BorrowForm(data=form_data)
        assert not form.is_valid()
        assert 'book' in form.errors