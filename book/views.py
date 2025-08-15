from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, Category
from .serializers import BookListModelSerializer, BookModelSerializer
from .serializers import AuthorModelSerializer
from .serializers import CategoryModelSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets

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
# class BookListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookModelSerializer

#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return BookListModelSerializer
#         return BookModelSerializer

#     def get_queryset(self):
#         author_name = self.request.query_params.get('author_name')
#         if author_name:
#             return self.queryset.filter(author__name=author_name)
#         return self.queryset

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     def perform_create(self, serializer): # perform_update, perform_destroy
    #         serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListModelSerializer
        return BookModelSerializer

    def get_queryset(self):
        author_name = self.request.query_params.get('author_name')
        if author_name:
            return self.queryset.filter(author__name=author_name)
        return self.queryset

# class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookModelSerializer

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


"""
get post put patch delete

get - data lazimdir (retrieve - bir obyekt #TODO BookModelSerializer(book), list- bir nece obyekt #TODO BookListModelSerializer(books, many=True)) - elave data lazim deyil. 
post - data lazim deyil (create) #TODO BookModelSerializer(data=request.data) - obyekt lazim deyil - ?
put - data lazimdir (update) #TODO BookModelSerializer(book, data=request.data) - bir obyekt lazimdir - elave data lazimdir
patch - data lazimdir (partial update) #TODO BookModelSerializer(book, data=request.data, partial=True) - bir obyekt lazimdir - elave data lazimdir.
delete - data lazimdir (destroy) #TODO Book.objects.get(id=id).delete() - bir obyekt lazimdir - elave data lazim deyil.


"""
    

# class AuthorListCreateAPIView(APIView):
#     def get(self, request):
#         authors = Author.objects.all()
#         serializer = AuthorModelSerializer(authors, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = AuthorModelSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class AuthorDetailAPIView(APIView):
#     def get(self, request, id):
#         author = get_object_or_404(Author, id=id)
#         serializer = AuthorModelSerializer(author)
#         return Response(serializer.data)

#     def put(self, request, id):
#         author = get_object_or_404(Author, id=id)
#         serializer = AuthorModelSerializer(author, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         author = get_object_or_404(Author, id=id)
#         author.delete()
#         return Response({'message': 'Author deleted successfully'},status=204)

# class CategoryListCreateAPIView(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategoryModelSerializer(categories, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = CategoryModelSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class CategoryDetailAPIView(APIView):
#     def get(self, request, id):
#         category = get_object_or_404(Category, id=id)
#         serializer = CategoryModelSerializer(category)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         category = get_object_or_404(Category, id=id)
#         serializer = CategoryModelSerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         category = get_object_or_404(Category, id=id)
#         category.delete()
#         return Response({'message': 'Category deleted successfully'},status=204)