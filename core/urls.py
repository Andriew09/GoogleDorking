from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_dork, name='generate_dork'),

]
