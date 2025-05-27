import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from library.models import Book, Author, Member, BorrowRecord

@pytest.mark.django_db
class TestAuthorModel:
    def test_create_author(self):
        author = Author.objects.create(
            first_name="John",
            last_name="Doe"
        )
        assert author.first_name == "John"
        assert str(author) == "John Doe"

@pytest.mark.django_db
class TestBookModel:
    def test_create_book(self, author):
        book = Book.objects.create(
            title="Sample Book",
            author=author,
            isbn="1234567890123",
            publication_date=timezone.now().date(),
            quantity=5,
            available=5
        )
        assert book.title == "Sample Book"
        assert book.available == 5
        assert str(book) == "Sample Book"

    def test_book_availability(self, book):
        assert book.is_available
        book.available = 0
        assert not book.is_available

@pytest.mark.django_db
class TestBorrowModel:
    def test_borrow_book(self, book, member):
        borrow = BorrowRecord.objects.create(
            book=book,
            member=member,
            due_date=timezone.now().date() + timezone.timedelta(days=14)
        )
        assert borrow.book == book
        assert not borrow.is_returned
        
        borrow.return_date = timezone.now().date()
        assert borrow.is_returned