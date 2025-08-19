from rest_framework import serializers
from .models import Book, Author, Category

class BookListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title','price', 'publication_date', 'language']
        read_only_fields = ['id']

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id','current_price'] 
        extra_kwargs = {
            'price':{
                'min_value':0
            },
            'publication_date':{'required':False, 'allow_null':True}
        }

class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
