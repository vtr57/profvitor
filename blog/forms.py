from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'texto',)

class PostFormCriar(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['texto']
        widgets = {
            'texto': forms.HiddenInput()
        }
