from django import forms

from .models import Homework, HomeworkDetail, Post

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['name', 'category', 'description', 'display', 'start_at', 'expired_date']

class HomeworkDetailForm(forms.ModelForm):
    class Meta:
        model = HomeworkDetail
        fields = '__all__'

class PostForm(forms.Form):
    github_url = forms.URLField(label="Ödev (URL)", max_length=100)