from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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
    CATEGORY_CHOICES = [
        ('FICTION', 'Fiction'),
        ('SCI-FI', 'Science Fiction'),
        ('BIOGRAPHY', 'Biography'),
        ('EDUCATION', 'Education')
    ]
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='FICTION'
    )
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class BorrowRecord(models.Model):
    """Model representing a book borrowing record."""
    BOOK_STATUS = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue')
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=BOOK_STATUS, default='BORROWED')
    def clean(self):
        # Prevent borrowing unavailable books
        if self.book.available <= 0:
            raise ValidationError("This book is not available for borrowing")
        
        # Check max borrows per user (3 books max)
        user_borrows = BorrowRecord.objects.filter(
            member=self.member,
            status='BORROWED'
        ).count()
        if user_borrows >= 3:
            raise ValidationError("You have reached the maximum borrowing limit (3 books)")
        
        # Prevent duplicate active borrows
        if BorrowRecord.objects.filter(
            book=self.book,
            member=self.member,
            status='BORROWED'
        ).exists():
            raise ValidationError("You have already borrowed this book")
    
    def __str__(self):
        return f"{self.member} borrowed {self.book} on {self.borrow_date}"

    def is_overdue(self):
        """Check if the borrowed book is overdue and not returned."""
        return date.today() > self.due_date and self.status != 'RETURNED'

    @property
    def is_returned(self):
        """Check if book has been returned."""
        return self.return_date is not None

    class Meta:
        ordering = ['-borrow_date']

# Example: Add reservation model
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled')
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reserved_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return f"{self.member}'s reservation for {self.book}"
    
    

# In the view, use the following to get or create a Member for the current user:
# member, created = Member.objects.get_or_create(user=request.user)