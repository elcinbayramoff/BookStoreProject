from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


"""
Book endpoints:
 - book list: lists all books
 - book detail: retrieves a specific book by ID
"""
router = DefaultRouter()
router.register('books', views.BookViewSet, basename='books')
router.register('author', views.AuthorViewSet, basename='author')
router.register('category', views.CategoryViewSet, basename='category')

urlpatterns = [
    # path('books/', views.BookListCreateAPIView.as_view()),
    # path('books/<int:id>/', views.BookDetailAPIView.as_view()),
    path('health_check/', views.HealthCheckAPIView.as_view()),
    path('author/', views.AuthorListCreateAPIView.as_view()),
    path('author/<int:id>/', views.AuthorDetailAPIView.as_view()),
    path('category/', views.CategoryListCreateAPIView.as_view()),
    path('category/<int:id>/', views.CategoryDetailAPIView.as_view()),
] 

urlpatterns += router.urls

"""
books/ - list
books/ - create
books/id/ - retrieve
books/id/ -update|partial_update
books/id/ -destroy
"""