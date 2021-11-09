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