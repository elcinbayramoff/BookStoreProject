from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Book

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


"""
If newly added category has the exact same name as the existing category,
then we should not allow to add it. 
"""