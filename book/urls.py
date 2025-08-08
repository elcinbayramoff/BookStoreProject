from django.urls import path
from . import views

"""
Book endpoints:
 - book list: lists all books
 - book detail: retrieves a specific book by ID
"""

urlpatterns = [
    path('books/', views.BookListCreateAPIView.as_view()),
    path('books/<int:id>/', views.BookDetailAPIView.as_view()),
    path('health_check/', views.HealthCheckAPIView.as_view()),
    path('author/', views.AuthorListCreateAPIView.as_view()),
    path('author/<int:id>/', views.AuthorDetailAPIView.as_view()),
]