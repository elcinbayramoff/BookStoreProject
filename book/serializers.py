from rest_framework import serializers
from .models import Book
from .models import Author, Category

class BookListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    publication_date = serializers.DateField()
    language = serializers.ChoiceField(choices=[
        ('EN', 'English'),
        ('AZ', 'Azerbaijani'),
        ('TR', 'Turkish'),
        ('RU', 'Russian'),
    ], default='EN')


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    publication_date = serializers.DateField()
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all(), required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    volume = serializers.IntegerField(default=1)
    language = serializers.ChoiceField(choices=[
        ('EN', 'English'),
        ('AZ', 'Azerbaijani'),
        ('TR', 'Turkish'),
        ('RU', 'Russian'),
    ], default='EN')
    stock_count = serializers.IntegerField(default=0)

    # def __init__(self, *args, **kwargs):
    #     from .models import Author, Category
    #     super().__init__(*args, **kwargs)
    #     self.fields['author'].queryset = Author.objects.all()
    #     self.fields['categories'].queryset = Category.objects.all()    

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        book = Book.objects.create(**validated_data)
        book.categories.set(categories)
        return book


    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', [])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if categories:
            instance.categories.set(categories)
        return instance

"""        setattr(instance,'title','Updated Title')
        instance.title = 'Updated Title'"""
        
   
class AuthorListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    
   

class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    biography = serializers.CharField(allow_null=True, allow_blank=True)
    name = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()


    def create(self, validated_data):
        author = Author.objects.create(**validated_data)
        return author


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    
class CategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)



    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
    

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

