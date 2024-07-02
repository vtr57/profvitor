from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import Post

class PostModelTests(TestCase):

    def setUp(self):
        # Criar um usuário para associar ao post
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='12345'
        )

        quill_content = '{"delta": "", "html": "Test Post"}'
        self.post = Post.objects.create(
            autor=self.user,
            titulo='Test Post',
            texto=quill_content,
            publicado_em=timezone.now()
        )

    def test_create_post(self):
        # Testa a criação de um post com QuillField
        self.assertEqual(self.post.autor.username, 'testuser')
        self.assertEqual(self.post.titulo, 'Test Post')
        self.assertEqual(self.post.texto.html, 'Test Post')
        self.assertIsNotNone(self.post.criado_em)
        self.assertIsNotNone(self.post.publicado_em)

    def test_publish_post(self):
        # Testa a publicação de um post
        self.assertIsNotNone(self.post.publicado_em)
        self.assertLessEqual(self.post.publicado_em, timezone.now())

    def test_post_str(self):
        # Testa a representação em string do post
        self.assertEqual(str(self.post), 'Test Post')
