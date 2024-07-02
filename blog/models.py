from django.conf import settings
from django.db import models
from django.utils import timezone
from django_quill.fields import QuillField

class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    texto = QuillField()
    criado_em = models.DateField(default=timezone.now)
    publicado_em = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.publicado_em = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.titulo