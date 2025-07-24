from django.db import models

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
        ...
    
    def __str__(self):
        return self.title
    
    def in_stock(self):
        return self.stock_count > 0
    
    def is_recent(self):
        from datetime import date, timedelta
        return (date.today() - self.publication_date) < timedelta(days=365)