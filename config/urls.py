from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def return_all_links(request):
    return HttpResponse('<a href="/api/books/">Books</a> <a href="/auth/login/">Login</a> <a href="/auth/register/">Register</a>')


urlpatterns = [
    path('', return_all_links),
    path('admin/', admin.site.urls),
    path('api/', include('book.urls')),
    path('auth/', include('user.urls')),
]

