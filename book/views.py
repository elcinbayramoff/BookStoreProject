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
from rest_framework import permissions
from .permissions import (
    CanManageBooks, 
    CanApplyDiscount, 
    CanManageAuthors, 
    CanManageCategories,
    IsSellerOrAdmin
)
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
    permission_classes = [permissions.IsAuthenticated, CanManageBooks]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListModelSerializer
        return BookModelSerializer

    def get_queryset(self):
        author_name = self.request.query_params.get('author_name')
        if author_name:
            return self.queryset.filter(author__name=author_name)
        return self.queryset
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any authenticated user to view books
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only sellers and admins can create/update/delete books
            permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]
        else:
            # For custom actions, use the default permissions
            permission_classes = self.permission_classes
        
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'], url_path='discount', permission_classes=[CanApplyDiscount])
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
    permission_classes = [permissions.IsAuthenticated, CanManageAuthors]
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any authenticated user to view authors
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only admins can create/update/delete authors
            permission_classes = [permissions.IsAuthenticated, CanManageAuthors]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'], url_path='change_name', permission_classes=[CanManageAuthors])
    def change_name(self, request, pk=None):
        author = self.get_object()
        new_name = request.data.get('name')
        serializer = self.get_serializer(author, {'name':new_name}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Author name changed successfully', 'author': AuthorModelSerializer(author).data})

    @action(detail=False, methods=['get'], url_path='by_name')
    def by_name(self, request):
        authors = self.queryset.order_by('name')
        return Response(self.get_serializer(authors, many=True).data)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageCategories]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, CanManageCategories]
        
        return [permission() for permission in permission_classes]

     
    
    @action(detail=True, methods=['post'], url_path='update_name', permission_classes=[CanManageCategories])
    def update_name(self, request, pk=None):
        category = self.get_object()
        new_name = request.data.get('name')
        serializer = self.get_serializer(category, {'name':new_name}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Category name updated successfully','category': CategoryModelSerializer(category).data})
    
    @action(detail=False, methods=['get'], url_path='by_name')
    def by_name(self, request):
        categories = self.queryset.order_by('name')
        return Response(self.get_serializer(categories, many=True).data)   
    
    
    
    
"""
get post put patch delete

get - data lazimdir (retrieve - bir obyekt #TODO BookModelSerializer(book), list- bir nece obyekt #TODO BookListModelSerializer(books, many=True)) - elave data lazim deyil. 
post - data lazim deyil (create) #TODO BookModelSerializer(data=request.data) - obyekt lazim deyil - ?
put - data lazimdir (update) #TODO BookModelSerializer(book, data=request.data) - bir obyekt lazimdir - elave data lazimdir
patch - data lazimdir (partial update) #TODO BookModelSerializer(book, data=request.data, partial=True) - bir obyekt lazimdir - elave data lazimdir.
delete - data lazimdir (destroy) #TODO Book.objects.get(id=id).delete() - bir obyekt lazimdir - elave data lazim deyil.


"""