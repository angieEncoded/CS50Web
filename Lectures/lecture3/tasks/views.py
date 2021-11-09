from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

# run python manage.py migrate to get the sessions working



# A way to create forms inside of django, django will create the html for this
class NewTaskForm(forms.Form):
    task = forms.CharField(label = "New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    # Set up a list of tasks per user session
    if "tasks" not in request.session:
        request.session["tasks"] = []


    return render(request, "tasks/index.html", {
        "tasks":request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        # Get all the data from the form
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })