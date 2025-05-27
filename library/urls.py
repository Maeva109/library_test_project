from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)

app_name = 'library'

urlpatterns = [
    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    
    # Book URLs
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('search/', views.book_search, name='book_search'),
    
    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/add/', views.MemberCreateView.as_view(), name='member_add'),
    path('members/<int:pk>/update/', views.MemberUpdateView.as_view(), name='member_update'),
    
    # Borrow URLs
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('borrow/list/', views.BorrowListView.as_view(), name='borrow-list'),
    path('borrow/<int:pk>/return/', views.return_book, name='return_book'),
    
    # Include API URLs
    path('api/', include(router.urls)),
]