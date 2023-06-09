import hashlib
import hmac
import json
import six
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes,force_str  
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.contrib.auth import get_user_model

User = get_user_model()

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk) + six.text_type(timestamp) +  
            six.text_type(user.is_active)  
        )  
account_activation_token = TokenGenerator()

def is_token_valid(user,token):
    return account_activation_token.check_token(user, token)

def user_from_uidb64(uidb64):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		return User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		return None
    

def send_mail(request,user,*,template,subject,reciver):
	message = render_to_string(template, {  
				'user': user,  
				'domain': get_current_site(request).domain,  
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
				'token':account_activation_token.make_token(user),
				"protocol": 'https' if request.is_secure() else 'http'  
			})  
	email = EmailMessage(  
			subject, message,from_email=settings.EMAIL_HOST_USER, to=[reciver]  
	)  
	return email.send()

def is_payment_valid(request_body : dict,payment_signature : str) -> bool:
	sorted_dict = dict(sorted(request_body.items()))
	#ignoring spaces is necessery for making a correct hash
	#python doc:To get the most compact JSON representation
	#you should specify (',', ':') to eliminate whitespace
	message = json.dumps(sorted_dict,separators=(',', ':'))
	calculated_signature = hmac.new(settings.NOWPAYMENTS_IPN_KEY.encode(), message.encode(), hashlib.sha512).digest().hex()
	return payment_signature == calculated_signature