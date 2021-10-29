# Authentication

- Django has auth built into the framework
- Create a users app that will track this stuff
  - python manage.py startapp users
- Go into the settings.py of the project and add the users project
```py
INSTALLED_APPS = [
    'users',
    'flights',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
- go into urls.py in the project and include the urls
```py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("flights/", include("flights.urls")),
    path("users/", include("users.urls"))
]
```

- Create the urls.py file in the app
```py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout")
]
```





