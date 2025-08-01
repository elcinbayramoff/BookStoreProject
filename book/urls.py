from django.urls import path
from . import views

"""
Book endpoints:
 - book list: lists all books
 - book detail: retrieves a specific book by ID
"""

urlpatterns = [
    path('books/', views.book_list_create),
    path('books/<int:id>/', views.book_detail),
]