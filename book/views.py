from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, Category
from .serializers import BookListModelSerializer, BookModelSerializer
from .serializers import AuthorModelSerializer
from .serializers import CategoryModelSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics


class HealthCheckAPIView(APIView):
    def get(self, request):
        return Response({'status':'ok'})
    

"""
list - get
retrieve - get
create - post
destroy - delete
update - put/patch
"""
#query_params = author_name
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListModelSerializer
        return BookModelSerializer

    def get_queryset(self):
        author_name = self.request.query_params.get('author_name')
        if author_name:
            return self.queryset.filter(author__name=author_name)
        return self.queryset
    
class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

class AuthorListCreateAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorModelSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AuthorDetailAPIView(APIView):
    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        serializer = AuthorModelSerializer(author)
        return Response(serializer.data)

    def put(self, request, id):
        author = get_object_or_404(Author, id=id)
        serializer = AuthorModelSerializer(author, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        author = get_object_or_404(Author, id=id)
        author.delete()
        return Response({'message': 'Author deleted successfully'},status=204)

class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CategoryDetailAPIView(APIView):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data)
    
    def put(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategoryModelSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response({'message': 'Category deleted successfully'},status=204)