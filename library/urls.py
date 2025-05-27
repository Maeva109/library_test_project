from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'books', views.BookViewSet, basename='book-api')

router.register(r'authors', views.AuthorViewSet, basename='author')

app_name = 'library'

urlpatterns = [

    # Include API URLs
    path('api/', include(router.urls)),

    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author-add'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # Book URLs
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/search/', views.BookSearchView.as_view(), name='book-search'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/add/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/add/', views.MemberCreateView.as_view(), name='member_add'),
    path('members/<int:pk>/update/', views.MemberUpdateView.as_view(), name='member_update'),
    
    # Borrow URLs
    path('borrows/', views.BorrowListView.as_view(), name='borrow-list'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow-book'),
    path('borrows/<int:borrow_id>/return/', views.return_book, name='return-book'),
    
    # Reservation URLs
    path('reservations/', views.ReservationListView.as_view(), name='reservation-list'),
    path('reservations/add/', views.ReservationCreateView.as_view(), name='reservation-add'),
    path('reservations/<int:pk>/cancel/', views.cancel_reservation, name='reservation-cancel'),
    # Registration URL
    path('register/', views.register, name='register'),
]