# Django notes
- Python web framework
  - Allows us to create web applications easily
- HTTP status codes
  - 200 - ok
  - 301 - Moved permanently
  - 403 - forbidden
  - 404 - Not found
  - 500 - internal server error
- Install Django
  - ```pip3 install Django```
- Create a new app
  - django-admin startproject PROJECT_NAME
  - important files
    - manage.py - this is what helps us run the server
    - settings.py - how the application behaves
    - url.py - table of contents for the web app
- Run the application
  - ```python manage.py runserver```
- Django project
  - one or more applications within the project
  - example
    - Google - 
      - image search
      - normal search
      - advanced search
      - these might all be separate apps
- Create a Django app after creating the project
  - ```python manage.py startapp NAMEOFAPP```
- Install the app into the project in settings.py
  - Add the app name to INSTALLED_APPS
- Now create the views for the app
  - Go into the app's views.py and define a function in order to serve up something for the app
```py
    from django.http import HttpResponse
    from django.shortcuts import render
    def index(request):
        return HttpResponse("Hello World")
```
- Now we need to create a urls.py file for the individual app
  - now define the url patterns
```py
    from django.urls import path
    from . import views

    urlpatterns = [
        # what path to visit, what view to render, optionally a string name to make it easy to reference later
        path("", views.index, name="index")
    ]
```
- Now go back to the project's urls.py location and add a path for the app
  - This is the 'master' urls map location
```py 
    from django.contrib import admin
    from django.urls import include, path
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("hello/", include("hello.urls"))
    ]
```
- Then the individual urls.py will send you to the right place
  - In this case, /hello which is a separate app
- Now we can create new functions that return things
```py
    def brian(request):
        return HttpResponse("Hello, Brian")
```
- Add that into the urlpatterns 
```py
    from django.urls import path
    from . import views

    urlpatterns = [
        # what path to visit, what view to render, optionally a string name to make it easy to reference later
        path("", views.index, name="index")
        path("brian", views.brian, name="brian")
    ]
```
- We can add an arbitrary number of functions
```py
    def david(request):
        return HttpResponse("Hello, David")
```
- Make sure to add that into the urls path as well
```py
    from django.urls import path
    from . import views

    urlpatterns = [
        # what path to visit, what view to render, optionally a string name to make it easy to reference later
        path("", views.index, name="index")
        path("brian", views.brian, name="brian")
        path("david", views.david, name="david")
    ]
```
- what if we want to have a dynamic page?
  - create a url pattern that will convert things like this
```py
    def greet(request, name):
        return HttpResponse(f"Hello, {name.capitalize()}")
```
- And all it to the urlpatterns file
```py
    from django.urls import path
    from . import views

    urlpatterns = [
        # what path to visit, what view to render, optionally a string name to make it easy to reference later
        path("", views.index, name="index")
        path("brian", views.brian, name="brian")
        path("david", views.david, name="david")
        path("<str:name>", views.greet, name="greet") # specify any string
    ]
```
- How to serve up html pages
  - instead of returning an HttpResponse, render a page
```py
    def index(request):
        return render(request, "hello/templatefile.html")
```
- Create a folder called hello, and then put the templates in there to namespace them
- We can also pass in parameters
  - Django has a templating language on top of the html
```py
    def greet(request, name):
        return render(request, "hello/greet.html" {
            "name": name
        })

```
- use {{}} inside of the html file to access variables
- conditionally show something in Django
```html
  {% if somevalue %}
    <h1>yes</h1>
  {% else %}
    <h1>no</h1>
  {% endif #}
```
- Django has a build system for how to handle static pages
  - Create a new folder called static
  - Then create a new folder with the same name as the app
  - Now all the css can go into this folder
- Add a command to the top of the file
```py 
{% load static }
```
- then include the link with this special Django syntax
```html
  <link href="{% static 'newyear/styles.css %}" rel="stylesheet>
``` 
- Django will work out the full path for itself
- Loops in templates
```html
    {% for task in tasks %}
      <li>{{task}}</li>
    {% empty %}
      <li>No Tasks</li>
    {% endfor %}
```
- Extending templates
- Create a layout.html with all the shared content
```html
  {% extends "tasks/layout.html" %}

  {% block body %}
  <h1>Tasks</h1>
  <ul>
      {% for task in tasks %}
      <li>{{task}}</li>
      {% empty %}
      <li>No Tasks</li>

      {% endfor %}
  </ul>
  <!-- We can dynamically tell it where to link to - this is done by name -->
  <!-- Tasks: is a way of namespacing the links -->
  <a href="{% url 'tasks:add' %}">Add task</a>
  {% endblock %}
```
- Dynamically figuring out routes
  - We can link to the name instead of a static route in files
  - <a href="{% url 'tasks:add' %}">Add task</a>

- csrf tokens
  - Django has this turned on by default with some middleware
  - We don't have to set this up ourselves
  - 


- FORMS in django
```py
  def add(request):
    return render(request, )

```


