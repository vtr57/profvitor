from django.contrib import admin
from .models import Post
from .models import Questao
from .models import Vestibular
from .models import Tema


class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'ano',)

admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Post)
admin.site.register(Vestibular)
admin.site.register(Tema)
