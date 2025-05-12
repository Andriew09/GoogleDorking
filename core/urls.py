from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_dork, name='generate_dork'),
    path('export/csv/', views.export_dorks_csv, name='export_dorks_csv'),
    path('export/json/', views.export_dorks_json, name='export_dorks_json'),

]
