from django.contrib import admin
from django.urls import path, include

urlpatterns = [
     path('admin/', admin.site.urls),
    path('api/', include('library.api_urls')),  # New separate API URLs
    path('library/', include(('library.urls', 'library'), namespace='library')),  # Add this prefix
    path('accounts/', include('django.contrib.auth.urls')),  # <-- Add this line
]