from django import template
from django.contrib.auth.models import Group 
from users.models import CustomUser

register = template.Library()

@register.filter(name='is_moderator')
def is_moderator(user, user_id):
    if user.is_staff:
        return True
    
    group = Group.objects.get(name='Moderator')
    user = CustomUser.objects.get(pk=int(user_id))
    return group in user.groups.all()

@register.filter(name='is_subscriber')
def is_subscriber(session_user, user_id): 
    group = Group.objects.get(name='Subscriber')
    target_user = CustomUser.objects.get(pk=int(user_id))
    return group in target_user.groups.all()