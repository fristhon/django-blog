from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from .forms import UserRegistrationForm

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('profile')

    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('login')
        
    return render(request, 'users/register.html', {'form':form})

def login(request):
    if request.user.is_authenticated:
            return HttpResponseRedirect('profile')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user:
            form = auth.login(request, user)
            print(request, f' Welcome {username} !!!!')
            return HttpResponseRedirect('profile')
    
    form = auth.forms.AuthenticationForm()
    return render(request, 'users/login.html', {'form':form, 'title':'log in'})

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login')
    return render(request, 'users/profile.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')