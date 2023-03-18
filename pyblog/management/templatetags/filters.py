from django import template
from django.contrib.auth.models import Group 
from users.models import CustomUser

register = template.Library()

@register.filter(name='is_subscriber')
def is_subscriber(session_user, user_id): 
    group = Group.objects.get(name='Subscriber')
    target_user = CustomUser.objects.get(pk=int(user_id))
    return group in target_user.groups.all()