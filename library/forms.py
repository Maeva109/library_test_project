from django import forms
from .models import Book, Author, Member, BorrowRecord
from django.core.exceptions import ValidationError

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        if not isbn.isdigit():
            raise ValidationError("ISBN must contain only digits.")
        if len(isbn) != 13:
            raise ValidationError("ISBN must be 13 digits long.")
        return isbn


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'member', 'due_date']
        
    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        if book and book.available <= 0:
            self.add_error('book', "This book is not available for borrowing.")
        return cleaned_data