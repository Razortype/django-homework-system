from django import forms

from .models import Homework, HomeworkDetail, Post

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['name', 'content', 'description', 'display', 'start_at', 'expired_date']

class HomeworkDetailForm(forms.ModelForm):
    class Meta:
        model = HomeworkDetail
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['person', 'post_url', 'post_url']

class NewPostForm(forms.Form):
    github_url = forms.URLField(required=True)