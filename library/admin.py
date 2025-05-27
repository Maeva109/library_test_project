from django.contrib import admin
from .models import Book, Author, Member, BorrowRecord

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Member)
admin.site.register(BorrowRecord)