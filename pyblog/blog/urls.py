from django.urls import path
from . import views

urlpatterns = [
    path('<slug:post_slug>/', views.post,name='post'),
]
