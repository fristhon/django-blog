from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group
from users.models import CustomUser
from blog.models import Post
from .values import EDITORSHIP_ACCESS_MSG
from .forms import UpdatePostForm

def editorship(request):
	user = request.user
	if not user.is_staff and not user.groups.filter(name ='Moderator').exists():
		messages.warning(request,EDITORSHIP_ACCESS_MSG)
		return HttpResponseRedirect('/')

	if request.method == 'GET':
		post_form = UpdatePostForm()
		posts = Post.objects.all()
		users = CustomUser.objects.all()
		return render(request,"management/editorship.html",{'form':post_form,'posts':posts,'users':users})

	payload = request.POST
	if "publish" in payload:
		post_form = UpdatePostForm(request.POST, request.FILES)
		if post_form.is_valid():
			post_form.save()
			messages.success(request,"Post Published successfully")
	elif "editpost" in payload:
		post_id = int(payload['editpost'])
		post = Post.objects.get(pk=post_id)
		post.vip = not post.vip
		post.save()

	elif "edituser" in payload:
		user_id = int(payload['edituser'])
		user = CustomUser.objects.get(pk=user_id)
		group_name = 'Subscriber'
		group = Group.objects.get(name=group_name) 
		if user.groups.filter(name=group_name).exists():
			user.groups.remove(group)
		else:
			user.groups.add(group)

	return HttpResponseRedirect("editorship")


