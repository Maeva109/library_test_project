import pytest
from django.contrib.auth.models import User
from library.models import Author, Book, Member

@pytest.fixture
def author():
    return Author.objects.create(first_name="Test", last_name="Author")

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="pass")

@pytest.fixture
def member(user):
    return Member.objects.create(user=user)

@pytest.fixture
def book(author):
    return Book.objects.create(
        title="Test Book",
        author=author,
        isbn="1234567890123",
        category="FICTION",
        quantity=2,
        available=2,
        publication_date="2024-01-01"
    )