from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(this):
        return f"{this.city} ({this.code})"

# Create your models here.
class Flight(models.Model):
    origin  = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    # Give back a string representation of this object
    # self is an arbitrary name, we can use this
    def __str__(this):
        return f"{this.id}: {this.origin} to {this.destination}"

class Passenger(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # set up a many to many relationship
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(this):
        return f"{this.first_name} {this.last_name}"