import pytest
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from library.models import Book, Author, Member, BorrowRecord, Reservation

@pytest.mark.django_db
class TestBookModel:
    def test_book_creation(self):
        author = Author.objects.create(first_name="Test", last_name="Author")
        book = Book.objects.create(
            title="Test Book",
            author=author,
            isbn="1234567890123",
            category="FICTION",
            quantity=5,
            available=5,
            publication_date="2024-01-01"
        )
        assert book.available == 5
        assert str(book) == "Test Book"

    def test_borrow_availability(self):
        author = Author.objects.create(first_name="Test", last_name="Author")
        book = Book.objects.create(
            title="Test",
            author=author,
            isbn="1234567890123",
            category="FICTION",
            quantity=1,
            available=1,
            publication_date="2024-01-01"
        )
        assert book.is_available
        book.available = 0
        assert not book.is_available

@pytest.mark.django_db
class TestBorrowRecord:
    def test_borrow_creation(self, book, member):
        borrow = BorrowRecord.objects.create(
            book=book,
            member=member,
            due_date=timezone.now() + timedelta(days=14)
        )
        assert borrow.status == 'BORROWED'
        
    def test_max_borrows(self, member, author):
        # Create 3 borrows
        for i in range(3):
            book = Book.objects.create(
                title=f"Book {i}",
                author=author,
                isbn=f"123456789012{i}",
                category="FICTION",
                quantity=1,
                available=1,
                publication_date="2024-01-01"
            )
            BorrowRecord.objects.create(
                book=book,
                member=member,
                due_date=timezone.now() + timedelta(days=14)
            )
        
        # Attempt 4th borrow
        new_book = Book.objects.create(
            title="New Book",
            author=author,
            isbn="1234567890000",
            category="FICTION",
            quantity=1,
            available=1,
            publication_date="2024-01-01"
        )
        with pytest.raises(ValidationError):
            BorrowRecord(
                book=new_book,
                member=member,
                due_date=timezone.now() + timedelta(days=14)
            ).full_clean()