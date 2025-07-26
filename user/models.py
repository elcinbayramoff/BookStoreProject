from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    birth_date = models.DateField()
    
    def __str__(self):
        return self.name
    
    def has_email(self):
        if self.email:
            return True
        return False
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # her istifadecinin yalniz bir profili ola biler  
    full_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user or self.full_name
    
    def has_phone(self):
        if self.phone:
            return True
        return False
    
    class Meta:
        ...
