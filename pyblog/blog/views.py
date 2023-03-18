from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post
from .values import POST_IS_VIP_MSG

def post(request,post_slug):
    post = get_object_or_404(Post,slug=post_slug)
    user = request.user
    if post.vip and not user.groups.filter(name ='Subscriber').exists():
        messages.warning(request,POST_IS_VIP_MSG)
        return HttpResponseRedirect("/users/login")

    return render(request,"blog/post.html",{'post':post})