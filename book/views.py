from rest_framework.response import Response
from .models import Book, Author, Category, Order, OrderItem
from .serializers import BookListModelSerializer, BookModelSerializer, OrderItemModelSerializer, OrderModelSerializer   
from .serializers import AuthorModelSerializer
from .serializers import CategoryModelSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
import decimal
from rest_framework import permissions, status
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from .permissions import (
    CanManageBooks, 
    CanApplyDiscount, 
    CanManageAuthors, 
    CanManageCategories,
    IsSellerOrAdmin,
    IsCustomerOrAdmin
)
from .paginators import CustomPageNumberPagination
from .filters import BookFilter


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
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    search_fields = ['title', 'description', 'author__name', 'categories__name']
    ordering_fields = ['price', 'publication_date', 'title', 'current_price', 'discount_percentage']
    ordering = ['-publication_date']
    pagination_class = CustomPageNumberPagination
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListModelSerializer
        return BookModelSerializer

    def get_queryset(self):
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
    

class OrderItemAPIView(APIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer
    permission_classes = [IsCustomerOrAdmin]

    def post(self, request):
        order = Order.objects.create(customer=request.user)
        data = request.data.copy()
        for item in data:
            item['order'] = order.id
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Order created successfully', 'order items':serializer.data})

class OrderAPIView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [IsCustomerOrAdmin]


    def get(self, request, pk=None):
        if pk:
            order = self.queryset.get(id=pk)
            if order.customer != request.user:
                return Response({'message': 'You are not authorized to view this order'}, status=status.HTTP_403_FORBIDDEN)
            return Response(self.serializer_class(order).data)

        orders = self.queryset.filter(customer=request.user)
        return Response(self.serializer_class(orders, many=True).data)
    
    def patch(self, request, pk=None):
        try:
            order = self.queryset.get(id=pk)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.customer != request.user:
            return Response({'message': 'You are not authorized to update this order'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Order updated successfully', 'order': serializer.data})
    
    
"""
get post put patch delete

get - data lazimdir (retrieve - bir obyekt #TODO BookModelSerializer(book), list- bir nece obyekt #TODO BookListModelSerializer(books, many=True)) - elave data lazim deyil. 
post - data lazim deyil (create) #TODO BookModelSerializer(data=request.data) - obyekt lazim deyil - ?
put - data lazimdir (update) #TODO BookModelSerializer(book, data=request.data) - bir obyekt lazimdir - elave data lazimdir
patch - data lazimdir (partial update) #TODO BookModelSerializer(book, data=request.data, partial=True) - bir obyekt lazimdir - elave data lazimdir.
delete - data lazimdir (destroy) #TODO Book.objects.get(id=id).delete() - bir obyekt lazimdir - elave data lazim deyil.


"""