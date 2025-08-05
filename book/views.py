from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .models import Author
from .models import Category
from datetime import date
from .serializers import BookListSerializer, BookSerializer
from django.shortcuts import get_object_or_404
from .serializers import AuthorSerializer, CategorySerializer

@api_view(['GET', 'POST'])
def book_list_create(request): 

    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        data = serializer.data
        return Response(data)
    

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        return Response(serializer.data, status=201)
    

@api_view(['GET','PUT','DELETE'])
def book_detail(request, id): # patch - partial update
    book = get_object_or_404(Book, id=id)
    if request.method == 'GET':
        try:
            book = Book.objects.get(id=id) # if .filter(id=id).exists():
            data = {
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'author': book.author.name,
                'publication_date': book.publication_date,
                'categories': [category.name for category in book.categories.all()],
                'price': str(book.price),
                'language': book.language,
                'stock_count': book.stock_count,
                'in_stock': book.in_stock(),
                'is_recent': book.is_recent(),
            }
            return Response(data)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            book = Book.objects.get(id=id)
            book.delete()
            return Response({'message': 'Book deleted successfully'}, status=204)

        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)
    
    elif request.method == 'PUT':
        try:
            book = Book.objects.get(id=id)
            data = request.data
            
            book.title = data.get('title', book.title)
            book.description = data.get('description', book.description)
            book.author_id = data.get('author_id', book.author_id)
            book.publication_date = data.get('publication_date', book.publication_date) # TODO: validate date format
            book.price = data.get('price', book.price)
            book.language = data.get('language', book.language)
            book.stock_count = data.get('stock_count', book.stock_count)

            book.save()
            categories = data.get('categories', [])
            if categories:
                book.categories.set(categories)
            """
            request_data = {
                "title": "Sefiller",
                "description": "A classic novel",
                "author_id": 19,
                "publication_date": "2025-04-04",
                "price": 19.99,
                "language": "AZ",
                "stock_count": 100,
                "categories": [1, 2, 3]  # Assuming these are category IDs
            }
            
            """
            return Response({
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'author': book.author.name,
                'publication_date': book.publication_date,
                'categories': [category.name for category in book.categories.all()],
                'price': str(book.price),
                'language': book.language,
                'stock_count': book.stock_count,
                'in_stock': book.in_stock(),
                'is_recent': book.is_recent(),
            })
        
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)


#books/5/ -POST AUTHOR

@api_view(['GET', 'POST'])
def author_list_create(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        name = request.query_params.get('name')  # /authors/?name=Victor
        if name:
            authors = authors.filter(name=name)

        data = []
        for author in authors:
            data.append({
                'id': author.id,
                'name': author.name,
                'birth_date': author.birth_date,
                'country': author.country
            })
        return Response(data)

    elif request.method == 'POST':
        data = request.data
        author = Author.objects.create(
            name=data['name'],
            birth_date=data['birth_date'],
            country=data['country']
        )
        """
        request data = {
            "name": "Victor Hugo",
            "birth_date": "1802-02-26",
            "country": "France"
        }
        
        """

        return Response({
            'id': author.id,
            'name': author.name,
            'birth_date': author.birth_date,
            'country': author.country
        })

@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, id):
    try:
        author = Author.objects.get(id=id)
    except Author.DoesNotExist:
        return Response({'error': 'Author not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': author.id,
            'name': author.name,
            'birth_date': author.birth_date,
            'country': author.country
        }
        return Response(data)

    elif request.method == 'PUT':
        data = request.data
        author.name = data.get('name', author.name)
        author.birth_date = data.get('birth_date', author.birth_date)
        author.country = data.get('country', author.country)
        author.save()

        return Response({
            'id': author.id,
            'name': author.name,
            'birth_date': author.birth_date,
            'country': author.country
        })

    elif request.method == 'DELETE':
        author.delete()
        return Response({'message': 'Author deleted successfully'}, status=204)


@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description
            })
        return Response(data)

    elif request.method == 'POST':
        data = request.data
        category = Category.objects.create(
            name=data['name'],
            description=data.get('description', '')
        )
        """
        request_data = {
            "name": "Drama",
            "description": "A classic novel"
        }
        
        """
        return Response({
            'id': category.id,
            'name': category.name,
            'description': category.description
        })

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }
        return Response(data)

    elif request.method == 'PUT':
        data = request.data

        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.save()

        """
        request_data = {
            "name": "Drama",
            "description": "Tragic and emotional stories"
        }
        
        """

        return Response({
            'id': category.id,
            'name': category.name,
            'description': category.description
        })

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=204)

@api_view(['GET', 'POST'])
def category_list_create(request): 

     if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(serializer.data, status=201)


