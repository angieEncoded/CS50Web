# Django models with SQL
- Set up a new app
  - django-admin startproject airline
  - open the project in code
  - add an 'app' into the project
  - python manage.py startapp flights
  - add the app to the flights settings.py
```py
INSTALLED_APPS = [
    'flights',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
  - Configure the urls.py
```py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("flights/", include("flights.urls"))
]
```
- Create urls.py file inside the application
```py
from django.urls import path
from . import views
urlpatterns = [
]
```
- create some models - a python class that django will use
- There is a models.py file by default
- one model per class
```py
from django.db import models

# Create your models here.
class Flight(models.Model):
    origin  = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

```
- Now you can tell django to update the database with the models we created
  - called 'migration'
- make the migration with a command
  - ```python manage.py makemigrations```
- Then tell it to migrate
  - ```python manage.py migrate```
- How to manipulate data with django
  - enter django's shell
  - ```python manage.py shell```
- Add a flight with django syntax
```py
$ python manage.py shell
Python 3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from flights.models import Flight
>>> f = Flight(origin="New York", destination="London", duration=415) 
>>> f.save()
```
- SELECT * 
```Flight.objects.all()```
<QuerySet [<Flight: Flight object (1)>]>

- Making it look nice 
  - We can add string representations of the object to format the select query
```py
    # Give back a string representation of this object
    # self is an arbitrary name, we can use this
    def __str__(this):
        return f"{this.id}: {this.origin} to {this.destination}"
```
  - note that the lecture used self - but this is arbitrary. It can be named 
  - this which I did here for my own comfort levels
- Get the first flight
  - ```flight - flights.first()```
  - Now we can access the properties
  - flight.origin
  - flight.destination
  - flight.duration
  - flight.delete()
- This works, but this isn't the ultimate end state for the database. We actually want this to be a nice joined table
```py
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

```
- Now we have to migrate these changes to the database
  - ```python manage.py makemigrations```
  - ```python manage.py migrate```
  - The database does need to be empty for this to work
- Now go back into the shell and import
  - ```python manage.py shell```
  - ```from flights.models import *```
- And now we can go back and add data
```py 
jfk = Airport(code="JFK", city="New York")
lhr = Airport(code="LHR", city="London")
cdg = Airport(code="CDG", city="Paris")
nrt = Airport(code="NRT", city="Tokyo")
jfk.save()
lhr.save()
cdg.save()
nrt.save()
# Create a flight
f = Flight(origin=jfk, destination=lhr, duration=415)
f.save()
```
- Now we can use the powerful abstraction features
  - Get details about the flight from the associated tables
    - f.origin
    - f.origin.code
    - f.origin.city
  - Get details about a certain airport without writing a join query
    - lhr.arrivals.all()
- Query the database with django
- - Get all the objects
  - ```Airport.objects.all()
- Get the first item in a set of records
  - ```Airport.objects.filter(city="New York").first()```
- If we know there is only one object use this 
  - Airport.objects.get(city="New York")
- Now we can create the Passengers model, and Django allows us to abstract away the Many to Many relationship
```py
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
```