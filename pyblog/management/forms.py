from django import forms
from blog.models import Post

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['slug']