from django.contrib import admin
<<<<<<< HEAD
from .models import Book,Author,Category
=======
from .models import Book
from .models import Author
from .models import Category

>>>>>>> 7abccbc48a9e48cc7ef2d5f95cd939cba07cd7d6
# Register your models here.

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'publication_date', 'price', 'current_price', 'discount_percentage']
#     list_filter = ['author', 'publication_date']
#     search_fields = ['title', 'author__name']
#     ordering = ['-publication_date']

def mark_as_depleted(modeladmin, request, queryset):
    queryset.update(stock_count=0)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author', 'publication_date', 'price', 'current_price', 'discount_percentage', 'stock_count']
    list_filter = ['author', 'publication_date']
    list_display_links = ['author']
    search_fields = ['title', 'author']
    ordering = ['-publication_date']
    actions = [mark_as_depleted]
    # fields = ['title', 'author', 'publication_date', 'price', 'current_price', 'discount_percentage']
    # read_only_fields = ['current_price']

<<<<<<< HEAD

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','author__name', 'publication_date', 'price', 'current_price', 'discount_percentage']
    list_filter = ['author', 'publication_date']
    list_display_links = ['author__name']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_date']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['title','author__name', 'publication_date', 'price', 'current_price', 'discount_percentage']
    list_filter = ['author', 'publication_date']
    list_display_links = ['author__name']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_date']
=======
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'biography']
    list_filter = ['birth_date']
    search_fields = ['name']
    ordering = ['name']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
>>>>>>> 7abccbc48a9e48cc7ef2d5f95cd939cba07cd7d6
