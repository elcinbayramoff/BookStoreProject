from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from datetime import date

@api_view(['GET', 'POST'])
def book_list_create(request): 
    if request.method == 'GET':
        books = Book.objects.all()
        author = request.query_params.get('author') #/books/?author=John
        if author:
            books = books.filter(author__name=author)
        
        data = []
        for book in books:
            data.append({
                'id': book.id,
                'title': book.title,
                'publication_date': book.publication_date,
                'price': str(book.price),
                'language': book.language
            })
        return Response(data)
    

    elif request.method == 'POST':
        data = request.data
        book = Book.objects.create(
            title=data['title'],
            author_id=data['author_id'],
            publication_date=data['publication_date'],
            price=data['price'],
            language=data['language']
        )
        """
        request data = {
            "title": "Sefiller",
            "author_id": 19,
            "publication_date": "2025-04-04",
            "price": 19.99,
            "language": "AZ",
        }
        
        """

        book.categories.set(data.get('categories', []))
        return Response({
            'id': book.id,
            'title': book.title,
            'publication_date': book.publication_date,
            'price': str(book.price),
            'language': book.language,
            'categories': [category.name for category in book.categories.all()]
        })
    

@api_view(['GET','PUT','DELETE'])
def book_detail(request, id): # patch - partial update
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