import pytest
import os
import django
from django.conf import settings

# Configure Django for tests
def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
    django.setup()

@pytest.fixture
def author():
    from library.models import Author
    return Author.objects.create(
        first_name="Test",
        last_name="Author"
    )

@pytest.fixture
def book(author):
    from library.models import Book
    return Book.objects.create(
        title="Test Book",
        author=author,
        isbn="1234567890123",
        publication_date="2023-01-01",
        quantity=5,
        available=5
    )

@pytest.fixture
def member():
    from library.models import Member
    return Member.objects.create(
        first_name="Test",
        last_name="Member",
        email="testmember@example.com"
    )
@pytest.fixture
def unavailable_book(author):
    from library.models import Book
    return Book.objects.create(
        title="Unavailable Book",
        author=author,
        isbn="9876543210123",
        publication_date="2023-01-01",
        quantity=0,  # No copies available
        available=0
    )
@pytest.fixture
def client():
    from django.test import Client
    return Client()
# ... rest of your fixtures ...

