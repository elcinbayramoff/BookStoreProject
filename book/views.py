from rest_framework.decorators import api_view
from rest_framework.response import Response

BOOKS = {
    1: {'id': 1, 'title': 'The Midnight Library', 'author': 'Matt Haig', 'page_count': 304},
    2: {'id': 2, 'title': 'Project Hail Mary', 'author': 'Andy Weir', 'page_count': 496},
    3: {'id': 3, 'title': 'The Silent Patient', 'author': 'Alex Michaelides', 'page_count': 336},
    4: {'id': 4, 'title': 'The Paris Library', 'author': 'Janet Skeslien Charles', 'page_count': 368},
    5: {'id': 5, 'title': 'Artemis', 'author': 'Andy Weir', 'page_count': 320},
    6: {'id': 6, 'title': 'Where the Crawdads Sing', 'author': 'Delia Owens', 'page_count': 384}
}

@api_view(['GET'])
def debug_view(request, id, word):
    my_param = request.query_params.get('my_param')
    return Response({"message": f"This is a debug view with the id {id} and word {word}.\nQuery parameters: {my_param}"}) 

@api_view(['GET'])
def book_list(request):
    author = request.query_params.get('author')
    books = BOOKS.values()
    if author:
        books = [book for book in books if book['author'] == author]
    return Response(books)

@api_view(['GET'])
def book_detail(request, id):
    book = BOOKS.get(id)
    if not book:
        return Response({"error": "Book not found"}, status=404)
    return Response(book)

"""
Eyni prosesi user üçün edəcəyik.
Users endpointləri:
    - user list: lists all users
    - user detail: retrieves a specific user by ID

"""