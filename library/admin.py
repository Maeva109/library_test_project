from django.contrib import admin
from .models import Book, Author, Member, BorrowRecord, Reservation

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Member)
admin.site.register(BorrowRecord)
admin.site.register(Reservation)