from django.contrib import admin
from .models import Book
# Register your models here.

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'publication_date', 'price', 'current_price', 'discount_percentage']
#     list_filter = ['author', 'publication_date']
#     search_fields = ['title', 'author__name']
#     ordering = ['-publication_date']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author__name', 'publication_date', 'price', 'current_price', 'discount_percentage']
    list_filter = ['author', 'publication_date']
    list_display_links = ['author__name']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_date']
    # fields = ['title', 'author', 'publication_date', 'price', 'current_price', 'discount_percentage']
    # read_only_fields = ['current_price']
