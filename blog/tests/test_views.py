from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models import Post

class PostListViewTests(TestCase):
    """
    Testes para a view post_list.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria dois posts que serão usados nos testes.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='12345'
        )
        Post.objects.create(autor=self.user,
                            titulo="Post 1",
                             texto='{"delta": "", "html": "Test Post"}',
                               publicado_em=timezone.now())
        Post.objects.create(autor=self.user,
                            titulo="Post 2",
                             texto='{"delta": "", "html": "Test Post2"}',
                               publicado_em=timezone.now())

    def test_post_list_view_status_code(self):
        """
        Verifica se a view retorna status 200.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template_used(self):
        """
        Verifica se o template correto é usado.
        """
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_view_context(self):
        """
        Verifica se o contexto contém a lista de posts e se a quantidade de posts é a esperada.
        """
        response = self.client.get(reverse('post_list'))
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 2)

class PostDetailViewTests(TestCase):
    """
    Testes para a view post_detail.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria um post que será usado nos testes.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='12345'
        )
        self.post = Post.objects.create(autor=self.user,
                                        titulo="Post 1",
                                         texto='{"delta": "", "html": "Test Post"}',
                                           publicado_em=timezone.now())

    def test_post_detail_view_status_code(self):
        """
        Verifica se a view retorna status 200.
        """
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_template_used(self):
        """
        Verifica se o template correto é usado.
        """
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_view_context(self):
        """
        Verifica se o contexto contém o post correto.
        """
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertTrue('post' in response.context)
        self.assertEqual(response.context['post'], self.post)

    def test_post_detail_view_404(self):
        """
        Verifica se a view retorna status 404 para um post inexistente.
        """
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
