from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class list_item(models.Model):
    seller=models.CharField(max_length=64)
    title=models.CharField(max_length=64)
    description=models.TextField()
    starting_bid=models.IntegerField()
    catagory=models.CharField(max_length=64)
    image=models.CharField(max_length=200, default=None, blank=True, null=True)
    createdat=models.DateTimeField(auto_now_add=True)

class bid(models.Model):
    user=models.CharField(max_length=64)
    newbid=models.IntegerField()
    title=models.CharField(max_length=64)
    item_id=models.IntegerField()

class watchlist(models.Model):
    user=models.CharField(max_length=64)
    item_id=models.IntegerField()

class comment(models.Model):
    user=models.CharField(max_length=64)
    item_id=models.IntegerField()
    content=models.TextField()
    createdon=models.DateTimeField(auto_now_add=True)

class winner(models.Model):

    name=models.CharField(max_length=64)
    seller=models.CharField(max_length=64)
    title=models.CharField(max_length=64,null=True)
    final_price=models.IntegerField()
