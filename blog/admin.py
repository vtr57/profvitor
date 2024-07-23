from django.contrib import admin
from .models import Post
from .models import Questao
from .models import Vestibular
from .models import Tema

admin.site.register(Post)
admin.site.register(Questao)
admin.site.register(Vestibular)
admin.site.register(Tema)
