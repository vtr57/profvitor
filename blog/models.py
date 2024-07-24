from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    criado_em = models.DateField(default=timezone.now)
    publicado_em = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.publicado_em = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.titulo
    
class Vestibular(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome
    
class Tema(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome

class Questao(models.Model):
    enunciado = models.TextField()
    imagem = models.ImageField(upload_to='img/questao/', blank=True, null=True)
    alternativas = models.TextField()
    ano = models.CharField(max_length=4)
    resposta = models.TextField()
    vestibular = models.ForeignKey(Vestibular, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.enunciado               