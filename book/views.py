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

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer

class CategoryViewSet(viewsets.ModelViewSet):
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