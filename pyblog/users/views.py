from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User  
from django.db.models import Q
from .forms import UserRegistrationForm,UserSetPasswordForm,UserPasswordResetForm
from .helpers import is_token_valid,send_mail,user_from_uidb64  

def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('profile')

	form = UserRegistrationForm()
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()

			send_mail(request,user,subject='Verify your email',template='users/activation_mail.html',reciver=form.cleaned_data.get('email'))
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


def activate(request, uidb64, token):
	user = user_from_uidb64(uidb64)
	if user is not None and is_token_valid(user, token):  
		user.is_active = True  
		user.save()  
		return HttpResponseRedirect('/')  
	return HttpResponse('Activation link is invalid!') 

def password_reset(request):
	if request.method == 'POST':
		form = UserPasswordResetForm(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data['email']
			user = User.objects.filter(Q(email=user_email)).first()
			if user:
				send_mail(request,user,subject='Password Reset request',template='users/password_reset_mail.html',reciver=user.email)

			return HttpResponseRedirect('/')

	form = UserPasswordResetForm()
	return render(request, 'users/password_reset.html', {"form": form})

def password_reset_confirm(request, uidb64, token):
	user = user_from_uidb64(uidb64)
	if user is not None and is_token_valid(user, token):
		if request.method == 'POST':
			form = UserSetPasswordForm(user, request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')

		form = UserSetPasswordForm(user)
		return render(request, 'users/password_reset_confirm.html', {'form': form})

	return HttpResponseRedirect("/")