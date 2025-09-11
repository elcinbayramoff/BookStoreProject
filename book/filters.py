from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    current_price_min = filters.NumberFilter(field_name='current_price', lookup_expr='gte')
    current_price_max = filters.NumberFilter(field_name='current_price', lookup_expr='lte')
    publication_date_after = filters.DateFilter(field_name='publication_date', lookup_expr='gte')
    publication_date_before = filters.DateFilter(field_name='publication_date', lookup_expr='lte')
    author_id = filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    author_name = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='categories__name', lookup_expr='icontains')
    language = filters.CharFilter(field_name='language', lookup_expr='iexact')
    in_stock = filters.BooleanFilter(method='filter_in_stock')
    
    class Meta:
        model = Book
        fields = []

    def filter_in_stock(self, queryset, name, value):
        if value is True:
            return queryset.filter(stock_count__gt=0)
        if value is False:
            return queryset.filter(stock_count__lte=0)
        return queryset