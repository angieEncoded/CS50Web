from django.contrib import admin
from .models import User, Email
from django.contrib.auth.admin import UserAdmin

class EmailAdmin(admin.ModelAdmin):
    list_display = ("user", "sender", "subject", "body", "timestamp", "read", "archived" )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)