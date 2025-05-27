from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from rest_framework import viewsets
from .models import Book, Author, Member, BorrowRecord, Reservation
from .forms import BookForm, AuthorForm, MemberForm, BorrowForm, UserRegisterForm
from .serializers import BookSerializer, AuthorSerializer
from django.utils import timezone
from django.contrib import messages
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Author Views
class AuthorListView(ListView):
    model = Author
    template_name = 'library/author_list.html'
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/author_detail.html'

class AuthorCreateView(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'birth_date', 'biography']
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:author-list')

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'birth_date', 'biography']
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:author-list')

class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'library/author_confirm_delete.html'
    success_url = reverse_lazy('library:author-list')

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
    success_url = reverse_lazy('library:book-list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:book-list')  # Redirect to the book list after saving


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

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
        books = books.filter(category=category)
    
    return render(request, 'library/book_search.html', {
        'books': books,
        'categories': Book.CATEGORY_CHOICES  # Pass choices to template
    })

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




class BorrowListView(ListView):
    model = BorrowRecord
    template_name = 'library/borrow_list.html'
    context_object_name = 'borrows'
    paginate_by = 10

    
# Borrow Views
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        if book.available > 0:
            # Get or create member profile for the user
            member, created = Member.objects.get_or_create(user=request.user)
            try:
                borrow = BorrowRecord(
                    book=book,
                    member=member,
                    due_date=date.today() + timedelta(days=14)
                )
                borrow.full_clean()
                borrow.save()
                book.available -= 1
                book.save()
                messages.success(request, 'Book borrowed successfully!')
                return redirect('library:book-list')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'No available copies to borrow')
    return render(request, 'library/borrow_confirm.html', {
        'book': book,
        'due_date': date.today() + timedelta(days=14)
    })

def return_book(request, borrow_id):
    borrow = get_object_or_404(BorrowRecord, pk=borrow_id)
    if request.method == 'POST':
        borrow.return_date = date.today()
        borrow.status = 'RETURNED'
        borrow.save()
        borrow.book.available += 1
        borrow.book.save()
        messages.success(request, 'Book returned successfully!')
        return redirect('library:borrow-list')
    return redirect('library:borrow-list')
    

# API Views
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save()

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# 
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Reservation

class ReservationListView(ListView):
    model = Reservation
    template_name = 'library/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(member=self.request.user.member)

class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['book']  # Member is automatically set
    template_name = 'library/reservation_form.html'

    def form_valid(self, form):
        form.instance.member = self.request.user.member
        form.instance.status = 'PENDING'
        messages.success(self.request, 'Reservation created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('library:reservation-list')

def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.status = 'CANCELLED'
        reservation.save()
        messages.success(request, 'Reservation cancelled successfully!')
    return redirect('library:reservation-list')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('library:book-list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def become_member(request):
    if hasattr(request.user, 'member'):
        messages.info(request, "You are already a member.")
        return redirect('library:book-list')
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, "You are now a library member!")
            return redirect('library:book-list')
    else:
        form = MemberForm()
    return render(request, 'library/member_form.html', {'form': form})

class BookSearchView(ListView):
    model = Book
    template_name = "library/book_search.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset