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
    path('health_check/', views.HealthCheckAPIView.as_view()),
] 

urlpatterns += router.urls

"""
books/ - list
books/ - create
books/id/ - retrieve
books/id/ -update|partial_update
books/id/ -destroy
"""