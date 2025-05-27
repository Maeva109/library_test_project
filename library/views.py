from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from rest_framework import viewsets
from .models import Book, Author, Member, BorrowRecord, Reservation
from .forms import BookForm, AuthorForm, MemberForm, BorrowForm
from .serializers import BookSerializer, AuthorSerializer
from django.utils import timezone


# Author Views
class AuthorListView(ListView):
    model = Author
    template_name = 'library/author_list.html'
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/author_detail.html'


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:author_list')


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:author_list')


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'library/author_confirm_delete.html'
    success_url = reverse_lazy('library:author_list')

# Book Views
class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book-list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book-list')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')


def book_search(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    return render(request, 'library/book_search.html', {'books': books, 'query': query})


# Member Views
class MemberListView(ListView):
    model = Member
    template_name = 'library/member_list.html'
    context_object_name = 'members'
    paginate_by = 10


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'library/member_form.html'
    success_url = reverse_lazy('library:member_list')


class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'library/member_form.html'
    success_url = reverse_lazy('library:member_list')


# Borrow Views
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow_record = form.save()
            book = borrow_record.book
            book.available -= 1
            book.save()
            return redirect('borrow-list')
    else:
        form = BorrowForm()
    return render(request, 'library/borrow_form.html', {'form': form})


def return_book(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk)
    if borrow_record.return_date is None:
        borrow_record.return_date = timezone.now().date()
        borrow_record.save()
        book = borrow_record.book
        book.available += 1
        book.save()
    return redirect('borrow-list')


class BorrowListView(ListView):
    model = BorrowRecord
    template_name = 'library/borrow_list.html'
    context_object_name = 'borrows'
    paginate_by = 10

# API Views
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_create(self, serializer):
        serializer.save()

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer



def book_search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )
    
    if category:
        books = books.filter(category__icontains=category)
    
    return render(request, 'library/book_search.html', {'books': books})


class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['book', 'member']
    template_name = 'library/reservation_form.html'
    success_url = reverse_lazy('reservation-list')

class ReservationListView(ListView):
    model = Reservation
    template_name = 'library/reservation_list.html'


class TestReservationViews:
    def test_create_reservation(self, client, book, member):
        url = reverse('reservation-add')
        response = client.post(url, {
            'book': book.id,
            'member': member.id
        })
        assert response.status_code == 302
        assert Reservation.objects.count() == 1

