from django.urls import path
from . import views

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'homepage'

urlpatterns = [
    path('', views.home, name="home"),
]
