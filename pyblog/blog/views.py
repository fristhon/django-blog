from django.shortcuts import render,get_object_or_404
from .models import Post

def post(request,post_slug):
    post = get_object_or_404(Post,slug=post_slug)
    return render(request,"blog/post.html",{'post':post})