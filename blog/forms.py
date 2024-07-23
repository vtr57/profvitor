from django import forms
from .models import Post
from .models import Questao

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'texto',)

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ("conteudo", "ano", "resposta", "vestibular", "tema", "imagem", )
