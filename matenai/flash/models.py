from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.

class User(AbstractUser):
    is_res = models.BooleanField('restaurant status', default=False)

class Restaurant(models.Model):
    res_id = models.ForeignKey(User, on_delete=CASCADE)
    res_name = models.CharField(max_length=20, primary_key=True)
    image_url = models.CharField(max_length=40)
    cuisine = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    zip_code = models.IntegerField()

class Menu(models.Model):
    res_id = models.ForeignKey(User, on_delete=CASCADE)
    item = models.CharField(max_length=40, primary_key=True)
    price = models.FloatField()

