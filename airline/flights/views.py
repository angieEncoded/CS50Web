from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Flight, Airport, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    # Django also supports pk=flight_id in case Primary Key is something else
    flight = Flight.objects.get(id=flight_id)


    return render(request, "flights/flight.html", {
        "flight": flight,
        # Django abstracts this away
        "passengers": flight.passengers.all(),
        # exclude passengers that are already on this flight  - this seemed to work even without the .all()
        "nonpassengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(id = flight_id)
        passenger = Passenger.objects.get(id = int(request.POST["passenger"]))
        # Django will add the user here
        passenger.flights.add(flight)
        #  This will allow us not to have to hard-code the redirect
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))