from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import UserRegistrationForm
from .tokens import account_activation_token  

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

            message = render_to_string('account_activation_mail.html', {  
                'user': user,  
                'domain': get_current_site(request).domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            mail_subject = 'Verify your email'
            email = EmailMessage(  
                    mail_subject, message,from_email=settings.EMAIL_HOST_USER, to=[form.cleaned_data.get('email') ]  
            )  
            email.send()
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


def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        # return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
        return HttpResponseRedirect('login')  
    else:
        return HttpResponse('Activation link is invalid!')  