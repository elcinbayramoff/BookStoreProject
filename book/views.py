from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .models import Author
from .models import Category
from datetime import date
from .serializers import BookListModelSerializer, BookModelSerializer
from .serializers import AuthorListSerializer, AuthorSerializer
from .serializers import CategoryListSerializer, CategorySerializer
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

@api_view(['GET', 'POST'])
def author_list_create(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorListSerializer(authors, many=True)
        data = serializer.data
        return Response(data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
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

