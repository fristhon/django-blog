from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from .forms import UserRegistrationForm,UserSetPasswordForm,UserPasswordResetForm
from .helpers import is_token_valid,send_mail,user_from_uidb64
from .values import EMAIL_CONFIRM_MSG
from .values import EMAIL_PROBLEM_MSG
from .values import LOGIN_MSG
from .values import LOGOUT_MSG
from .values import ACOUNT_ACTIVATION_MSG
from .values import INVALID_ACTIVATION_LINK_MSG
from .values import EMAIL_PASSWORD_RESET_MSG
from .values import PASSWORD_CHANGE_MSG
from .values import INVALID_PASSWORD_RESET_LINK_MSG

User = get_user_model()

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

			user_mail = form.cleaned_data.get('email')
			mail_result = send_mail(request,user,subject='Verify your email',template='users/activation_mail.html',reciver=user_mail)
			if mail_result:
				messages.success(request, EMAIL_CONFIRM_MSG.format(user))
			else:
				messages.error(request, EMAIL_PROBLEM_MSG.format(user_mail))

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
			messages.success(request,LOGIN_MSG.format(user))
			return HttpResponseRedirect('profile')
	
	form = auth.forms.AuthenticationForm()
	return render(request, 'users/login.html', {'form':form, 'title':'log in'})

def profile(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('login')
	return render(request, 'users/profile.html', {})

def logout(request):
	auth.logout(request)
	messages.info(request, LOGOUT_MSG)
	return HttpResponseRedirect('/')


def activate(request, uidb64, token):
	user = user_from_uidb64(uidb64)
	if user is not None and is_token_valid(user, token):  
		user.is_active = True  
		user.save()
		messages.success(request, ACOUNT_ACTIVATION_MSG)  
	else:
		messages.error(request, INVALID_ACTIVATION_LINK_MSG)

	return HttpResponseRedirect('/')

def password_reset(request):
	if request.method == 'POST':
		form = UserPasswordResetForm(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data['email']
			user = User.objects.filter(Q(email=user_email)).first()
			if user:
				mail_result = send_mail(request,user,subject='Password Reset request',template='users/password_reset_mail.html',reciver=user.email)
				if mail_result:
					messages.success(request,EMAIL_PASSWORD_RESET_MSG)
				else:
					messages.error(request, EMAIL_PROBLEM_MSG.format(user.mail))

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
				messages.success(request,PASSWORD_CHANGE_MSG)
				return HttpResponseRedirect('/')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)

		form = UserSetPasswordForm(user)
		return render(request, 'users/password_reset_confirm.html', {'form': form})
	
	else:
		messages.error(request, INVALID_PASSWORD_RESET_LINK_MSG)
		return HttpResponseRedirect("/")