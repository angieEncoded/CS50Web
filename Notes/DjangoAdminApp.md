# Django admin app
- A way to manage databases the Django way
- We need to create an admin account
``` python manage.py createsuperuser```
- Add the models to the admin app in admin.py
```py
from django.contrib import admin

from .models import Flight, Airport
# Register your models here.

admin.site.register(Airport)
admin.site.register(Flight)
```
- Now we can log into Django's admin interface at /project/admin
- Looks like just a front end
- Django was created for news orgs that wanted to be able to post quickly
- We have the ability to adjust the admin interface as well
```py
from django.contrib import admin

from .models import Flight, Airport, Passenger
# Register your models here.
# custom config - tell it we want to see all the fields
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

# This is helpful for handling the ones with many to many relationships
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)


```