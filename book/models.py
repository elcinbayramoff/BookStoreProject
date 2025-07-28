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

        return (date.today() - self.publication_date) < timedelta(days=365)

    

#operations
"""
create +
 a1 = Author.objects.create()
read
update
delete
"""
"""
python manage.py shell
In [1]: from book.models import Author, Category, Book

In [2]: Author.objects.all()
Out[2]: <QuerySet []>

In [3]: a1 = Author.objects.create('name'='Ali )
  Cell In[3], line 1
    a1 = Author.objects.create('name'='Ali )
                                      ^
SyntaxError: unterminated string literal (detected at line 1)


In [4]: from datetime import date

In [5]: 

In [5]: a1 = Author.objects.create(name='Ali', birth_date=date(1975,10,16)
   ...: )

In [6]: a1
Out[6]: <Author: Ali>

In [7]: a1 = Author.objects.create(name='Vali', birth_date=date(1950,10,16))

In [8]: c1 = Category.objects.create('Romantic')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[8], line 1
----> 1 c1 = Category.objects.create('Romantic')

File ~/.local/lib/python3.12/site-packages/django/db/models/manager.py:85, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     84 def manager_method(self, *args, **kwargs):
---> 85     return getattr(self.get_queryset(), name)(*args, **kwargs)

TypeError: QuerySet.create() takes 1 positional argument but 2 were given

In [9]: c1 = Category.objects.create(name='Romantic')

In [10]: c1
Out[10]: <Category: Romantic>

In [11]: c2 = Category.objects.create(name='Comedy')

In [12]: c2
Out[12]: <Category: Comedy>

In [13]: b1 = Book.objects.create(
    ...: title="Romeo and Julietta",
    ...: author=a1,
    ...: publication_date=date(2024, 4, 4)
    ...: ,price=9.99,
    ...: language='EN')

In [14]: b1
Out[14]: <Book: Romeo and Julietta>

In [15]: a2 = Author.objects.create(name='Ali', birth_date=date(1975,10,16)
    ...: )

In [16]: a1
Out[16]: <Author: Vali>

In [17]: a2
Out[17]: <Author: Ali>

In [18]: b1 = Book.objects.create(
    ...: title="Sefiller",
    ...: author=a1,
    ...: publication_date=date(2025, 4, 4)
    ...: ,price=19.99,
    ...: language='AZ')

In [19]: b1 = Book.objects.create(
    ...: title="Romeo and Julietta",
    ...: author=a1,
    ...: publication_date=date(2024, 4, 4)
    ...: ,price=9.99,
    ...: language='EN')

In [20]: b2 = Book.objects.create(
    ...: title="Sefiller",
    ...: author=a1,
    ...: publication_date=date(2025, 4, 4)
    ...: ,price=19.99,
    ...: language='AZ')

In [21]: Book.objects.all()
Out[21]: <QuerySet [<Book: Romeo and Julietta>, <Book: Sefiller>, <Book: Romeo and Julietta>, <Book: Sefiller>]>

In [22]: Book.objects.filter(id__in=[1,2]).delete()
Out[22]: (2, {'book.Book': 2})

In [23]: Book.objects.all()
Out[23]: <QuerySet [<Book: Romeo and Julietta>, <Book: Sefiller>]>

In [24]: b1.categories.add
Out[24]: <bound method create_forward_many_to_many_manager.<locals>.ManyRelatedManager.add of <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x766a0ea9c080>>

In [25]: b1.categories.add(c1)

In [26]: b1.categories.add(c2)

In [27]: b1.categories.all()
Out[27]: <QuerySet [<Category: Romantic>, <Category: Comedy>]>

In [28]: b1.categories.set([c1])

In [29]: b1.categories.all()
Out[29]: <QuerySet [<Category: Romantic>]>

In [30]: b1.categories.remove(c1)

In [31]: b1.categories.all(
    ...: )
Out[31]: <QuerySet []>

In [32]: b1.categories.add(c1)

In [33]: b1.categories.add(c2)

In [34]: b1.categories.clear()

In [35]: b1.categories.all(
    ...: )
Out[35]: <QuerySet []>

In [36]: b1.categories.add(c1)

In [37]: b1.language
Out[37]: 'EN'

In [38]: b1.price
Out[38]: 9.99

In [39]: b1.stock_count
Out[39]: 0

In [40]: Book.objects.all()
Out[40]: <QuerySet [<Book: Romeo and Julietta>, <Book: Sefiller>]>

In [41]: Book.objects.filter(language='AZ')
Out[41]: <QuerySet [<Book: Sefiller>]>

In [42]: Book.objects.get(id=1)
---------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
Cell In[42], line 1
----> 1 Book.objects.get(id=1)

File ~/.local/lib/python3.12/site-packages/django/db/models/manager.py:85, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     84 def manager_method(self, *args, **kwargs):
---> 85     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/.local/lib/python3.12/site-packages/django/db/models/query.py:496, in QuerySet.get(self, *args, **kwargs)
    494     return clone._result_cache[0]
    495 if not num:
--> 496     raise self.model.DoesNotExist(
    497         "%s matching query does not exist." % self.model._meta.object_name
    498     )
    499 raise self.model.MultipleObjectsReturned(
    500     "get() returned more than one %s -- it returned %s!"
    501     % (
   (...)    504     )
    505 )

DoesNotExist: Book matching query does not exist.

In [43]: Book.objects.get(id=2)
---------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
Cell In[43], line 1
----> 1 Book.objects.get(id=2)

File ~/.local/lib/python3.12/site-packages/django/db/models/manager.py:85, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     84 def manager_method(self, *args, **kwargs):
---> 85     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/.local/lib/python3.12/site-packages/django/db/models/query.py:496, in QuerySet.get(self, *args, **kwargs)
    494     return clone._result_cache[0]
    495 if not num:
--> 496     raise self.model.DoesNotExist(
    497         "%s matching query does not exist." % self.model._meta.object_name
    498     )
    499 raise self.model.MultipleObjectsReturned(
    500     "get() returned more than one %s -- it returned %s!"
    501     % (
   (...)    504     )
    505 )

DoesNotExist: Book matching query does not exist.

In [44]: Book.objects.get(id=3)
Out[44]: <Book: Romeo and Julietta>

In [45]: Book.objects.get(id=4)
Out[45]: <Book: Sefiller>

In [46]: Book.objects.filter(price__lt=25)
Out[46]: <QuerySet [<Book: Romeo and Julietta>, <Book: Sefiller>]>


"""
