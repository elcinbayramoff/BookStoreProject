from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Book
from .models import Category

@receiver(post_save, sender=Book)
def inform_about_new_book(sender, instance, created, **kwargs):
    if created:
        print('New book is created with title: ', instance.title)
    else:
        print('New book is updated with title: ', instance.title)


@receiver(pre_save, sender=Book)
def validate_book_price(sender, instance, **kwargs):
    price = instance.price
    if price < 0:
        raise ValueError('Price cannot be negative')


@receiver(post_save, sender=Category)
def inform_about_new_category(sender, instance, created, **kwargs):
    if created:
        print('New category is created with name: ', instance.name)
    else:
        print('New category is updated with name: ', instance.name)
        

@receiver(pre_save, sender=Category)
def validate_category_name(sender, instance, **kwargs):
    if Category.objects.filter(name=instance.name).exclude(id=instance.id).exists():
        raise ValueError('Category name already exists')
        

"""
If newly added category has the exact same name as the existing category,
then we should not allow to add it. 
"""