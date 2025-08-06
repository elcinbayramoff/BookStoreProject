from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .models import Author
from .models import Category
from datetime import date
from .serializers import BookListModelSerializer, BookModelSerializer
from .serializers import AuthorListModelSerializer, AuthorModelSerializer
from .serializers import CategoryListModelSerializer, CategoryModelSerializer, CategoryListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    def get(self, request):
        return Response({'status':'ok'})
    

# @api_view(['GET', 'POST'])
# def book_list_create(request):
#     if request.method == 'GET':
#         books = Book.objects.all()
#         serializer = BookListModelSerializer(books, many=True)
#         data = serializer.data
#         return Response(data)
    

#     elif request.method == 'POST':
#         serializer = BookModelSerializer(data=request.data)
#         # if not serializer.is_valid():
#         #     return Response(serializer.errors, status=400)
#         serializer.is_valid(raise_exception=True)
#         book = serializer.save()
#         return Response(serializer.data, status=201)
    
class BookListCreateAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookListModelSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail(request, id):
#     book = get_object_or_404(Book, id=id)

#     if request.method == 'GET':
#         serializer = BookModelSerializer(book)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = BookModelSerializer(book, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     elif request.method == 'DELETE':
#         book.delete()
#         return Response({'message': 'Book deleted successfully'},status=204)


class BookDetailAPIView(APIView):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookModelSerializer(book)
        return Response(serializer.data)   

    def put(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookModelSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)    

    def delete(self, request, id):
        book = get_object_or_404(Book, id=id)
        book.delete()
        return Response({'message': 'Book deleted successfully'},status=204)


#books/5/ -POST AUTHOR

class AuthorListCreateAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorListModelSerializer(authors, many=True)
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

@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'},status=204)

