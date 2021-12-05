from typing import ContextManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    summary = models.TextField(null=True, blank=True, default="User did not provide a summary!")
    number_of_followers = models.IntegerField(null=False, default=0)
    number_of_following = models.IntegerField(null=False, default=0)
    pass

class Post(models.Model):
    id= models.AutoField(primary_key=True)
    content= models.CharField(max_length=100)
    posted_by= models.ForeignKey(User, on_delete=CASCADE, related_name="posted_by_user")
    number_of_likes= models.IntegerField(null=False, default=0)
    posted_on= models.DateTimeField(auto_now_add=True)
    modified_on= models.DateTimeField(auto_now=True)

class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user") # the user this entry applies to
    following = models.ForeignKey(User, on_delete=SET_NULL, related_name="followed_user", null=True, blank=True)

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="post_likes") # the posts this entry applies to
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_likes") # the user this entry applies to