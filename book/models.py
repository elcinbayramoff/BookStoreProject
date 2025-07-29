from django.db import models
from pkg_resources import require

# author 5 - book 3, book 4 -
# Cascade - author deletion will delete all their books
# PROTECT - author deletion will be prevented if they have books
# SET_NULL - author deletion will set the author field of their books to NULL
# SET_DEFAULT - author deletion will set the author field of their books to a default value
# DO_NOTHING - author deletion will do nothing to their books


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(null=True, blank=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    publication_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    volume = models.PositiveSmallIntegerField(default=1)
    language = models.CharField(max_length=255, choices=[
        ('EN', 'English'),
        ('AZ', 'Azerbaijani'),
        ('TR', 'Turkish'),
        ('RU', 'Russian'),
    ], default='EN')
    stock_count = models.IntegerField(default=0)
    class Meta:
        # ordering = ['-publication_date']
        # verbose_name_plural = 'Books'
        # verbose_name = 'Book'
        # db_table = 'book'
        ...
    
    def __str__(self):
        return self.title
    
    def in_stock(self):
        return self.stock_count > 0
    
    def is_recent(self):
        from datetime import date, timedelta
        return (date.today() - self.publication_date) < timedelta(days=365)

    

#operations
"""
# Create
from book.models import Author, Book, Category
from datetime import date
a1 = Author.objects.create(name='Ali', birth_date=date(1975, 10, 16))
a1 = Author.objects.create(name='Vali', birth_date=date(1950, 10, 16))
a2 = Author.objects.create(name='Ali', birth_date=date(1975, 10, 16))
c1 = Category.objects.create(name='Romantic')
c2 = Category.objects.create(name='Comedy')
b1 = Book.objects.create(title="Romeo and Julietta", author=a1, publication_date=date(2024, 4, 4), price=9.99, language='EN')
b2 = Book.objects.create(title="Sefiller", author=a1, publication_date=date(2025, 4, 4), price=19.99, language='AZ')

# Update
b1.stock_count = 10
b1.price = 15.99
b1.save()

# Read
Author.objects.all()
Book.objects.all()
Book.objects.filter(id__in=[1, 2])
Book.objects.filter(language='AZ')
Book.objects.filter(price__lt=25)
Book.objects.get(id=3)
Book.objects.get(id=4)
b1.categories.all()
b1.language
b1.price
b1.stock_count

# Update (M2M)
b1.categories.add(c1)
b1.categories.add(c2)
b1.categories.set([c1])
b1.categories.remove(c1)
b1.categories.clear()
b1.categories.add(c1)

# Delete
Book.objects.filter(id__in=[1, 2]).delete()

"""

"""
# Create
category1 = Category.objects.create(name='Romantic')
Category.objects.create(name='Romantic')

# Read / Query
Category.objects.all()
Category.objects.all()[4]
Category.objects.all()[5].id
Category.objects.all().first()
Category.objects.all().last()
Category.objects.all().first().id
Category.objects.all().last().id
Category.objects.all().exists()
len(Category.objects.all())

category1.name
category1.id
category1.__dict__

# Delete
category1.delete()
Category.objects.all().delete()


"""