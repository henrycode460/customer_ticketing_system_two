# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True , null=True)
    cover_photo = models.ImageField(upload_to='profile_photos', blank=True , null=True)
    profile_photo = models.ImageField(upload_to='cover_photos', blank=True, null=True )
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=150, blank=True, null=True )
    address = models.CharField(max_length=150, blank=True, null=True )
   
    
    id = models.BigAutoField(primary_key=True)
    is_admin= models.BooleanField('Is admin', default=False)
    is_technician = models.BooleanField('Is technician', default=False)
    is_customer_care = models.BooleanField('Is customer care', default=False)
    is_employe = models.BooleanField('Is employee', default=False)
    is_supervisor = models.BooleanField('Is supervisor', default=False)
    is_logged_in = models.BooleanField(default=False)
