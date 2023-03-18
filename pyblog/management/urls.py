from django.urls import path
from . import views

urlpatterns = [
    path('editorship', views.editorship,name='editorship'),
]
