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
from rest_framework.decorators import action
import decimal

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
    
    @action(detail=True, methods=['post'], url_path='discount')
    def apply_discount(self, request, pk=None):
        # book = self.queryset.filter(id=pk).first() # method 1
        # book = self.queryset.get(id=pk) # method 2
        book = self.get_object() # method 3
        discount_percentage = request.data.get('discount_percentage', 0)
        book.current_price = book.price * decimal.Decimal(1-discount_percentage/100)
        book.discount_percentage = discount_percentage
        book.save()
        return Response({'message': 'Discount applied successfully', 'book': BookModelSerializer(book).data})

    @action(detail=False, methods=['get'], url_path='most_discounted_books')
    def order_most_discounted_books(self, request):
        books = self.queryset.order_by('-discount_percentage')
        return Response(self.get_serializer(books, many=True).data)



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


    @action(detail=True, methods=['post'], url_path='discount')
    def apply_discount(self, request, pk=None):
  
        author = self.get_object() # method 3
        discount_percentage = request.data.get('discount_percentage', 0)
        author.current_price = author.price * decimal.Decimal(1-discount_percentage/100)
        author.discount_percentage = discount_percentage
        author.save()
        return Response({'message': 'Discount applied successfully', 'author': AuthorModelSerializer(author).data})

    @action(detail=False, methods=['get'], url_path='most_discounted_authors')
    def order_most_discounted_authors(self, request):
        authors = self.queryset.order_by('-discount_percentage')
        return Response(self.get_serializer(authors, many=True).data)




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


    @action(detail=True, methods=['post'], url_path='discount')
    def apply_discount(self, request, pk=None):
       
        category = self.get_object() # method 3
        discount_percentage = request.data.get('discount_percentage', 0)
        category.current_price = category.price * decimal.Decimal(1-discount_percentage/100)
        category.discount_percentage = discount_percentage
        category.save()
        return Response({'message': 'Discount applied successfully', 'category': CategoryModelSerializer(category).data})

    @action(detail=False, methods=['get'], url_path='most_discounted_categorys')
    def order_most_discounted_categorys(self, request):
        categorys = self.queryset.order_by('-discount_percentage')
        return Response(self.get_serializer(categorys, many=True).data)



"""
get post put patch delete

get - data lazimdir (retrieve - bir obyekt #TODO BookModelSerializer(book), list- bir nece obyekt #TODO BookListModelSerializer(books, many=True)) - elave data lazim deyil. 
post - data lazim deyil (create) #TODO BookModelSerializer(data=request.data) - obyekt lazim deyil - ?
put - data lazimdir (update) #TODO BookModelSerializer(book, data=request.data) - bir obyekt lazimdir - elave data lazimdir
patch - data lazimdir (partial update) #TODO BookModelSerializer(book, data=request.data, partial=True) - bir obyekt lazimdir - elave data lazimdir.
delete - data lazimdir (destroy) #TODO Book.objects.get(id=id).delete() - bir obyekt lazimdir - elave data lazim deyil.


"""