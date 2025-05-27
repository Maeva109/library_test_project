from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(13)]
    )
    publication_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=20, choices=[
        ('FICTION', 'Fiction'),
        ('SCI-FI', 'Science Fiction'), 
        ('BIOGRAPHY', 'Biography'),
        ('EDUCATION', 'Education')]
    ,null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        """Check if book is available for borrowing."""
        return self.available > 0

    class Meta:
        ordering = ['title']


class Member(models.Model):
    """Model representing a library member."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class BorrowRecord(models.Model):
    """Model representing a book borrowing record."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    
    def __str__(self):
        return f"{self.book} borrowed by {self.member}"

    @property
    def is_returned(self):
        """Check if book has been returned."""
        return self.return_date is not None

    class Meta:
        ordering = ['-borrow_date']

# Example: Add reservation model
class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ], default='PENDING')

    def __str__(self):
        return f"{self.member}'s reservation for {self.book}"