from django.urls import path
from . import views

"""
Book endpoints:
 - book list: lists all books
 - book detail: retrieves a specific book by ID
"""

urlpatterns = [
    path('debug/<int:id>/<str:word>/', views.debug_view),
    path('books/', views.book_list),
    path('books/<int:id>/', views.book_detail),
]