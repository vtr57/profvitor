from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


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


class AuthViewsTest(TestCase):

    def setUp(self):
        """
        Set up the test environment.
        Create a test user and initialize the client.
        """
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_login_view_get(self):
        """
        Test the GET request to the login view.
        It should return a 200 status code and render the login template.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_login_view_post_valid(self):
        """
        Test the POST request to the login view with valid credentials.
        It should log the user in and redirect to the 'painel' page.
        """
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('painel'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        """
        Test the POST request to the login view with invalid credentials.
        It should return a 200 status code and render the login template with an error.
        """
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login.html')
        self.assertContains(response, 'Usuário ou Senha inválidas')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_painel_view_authenticated(self):
        """
        Test the GET request to the painel view for an authenticated user.
        It should return a 200 status code and render the painel template.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('painel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/painel.html')

    def test_painel_view_unauthenticated(self):
        """
        Test the GET request to the painel view for an unauthenticated user.
        It should redirect the user to the login page.
        """
        response = self.client.get(reverse('painel'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('painel')}")

    def test_logout_view(self):
        """
        Test the GET request to the logout view.
        It should log the user out and redirect to the login page.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)