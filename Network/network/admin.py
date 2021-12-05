from django.contrib import admin
from .models import User, Post, Follower, Like
from django.contrib.auth.admin import UserAdmin

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "posted_by", "number_of_likes", "posted_on", "modified_on")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "summary", "number_of_followers", "number_of_following")

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "following")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Like, LikeAdmin)
