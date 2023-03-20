from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("password_reset", views.password_reset, name="password_reset"),
    path('reset/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('payment',views.payment,name='payment'),
    path('payment_listner',views.payment_listner,name='payment_listner'),
]   