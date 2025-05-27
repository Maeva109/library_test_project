from django.contrib import admin
from .models import Book, Author, Member, BorrowRecord, Reservation

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Member)

admin.site.register(Reservation)

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'borrow_date', 'due_date', 'status')
    list_filter = ('status', 'borrow_date')
    search_fields = ('book__title', 'member__user__username')