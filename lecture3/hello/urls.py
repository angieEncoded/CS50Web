# import the pathmaker
from django.urls import path

# import the views directory
from . import views

# Set up a patterns list
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david")
]