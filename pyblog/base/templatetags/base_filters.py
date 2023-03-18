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