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

class CriarPostViewTest(TestCase):

    def setUp(self):
        # Configurar um cliente de teste
        self.client = Client()
        
        # Criar um usuário para autenticar
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # URL para a view de criação de post
        self.url = reverse('criar_post')

    def test_criar_post_view_get(self):
        """
        Verifica se a view responde corretamente a uma solicitação GET,
        utilizando o template correto e incluindo o formulário no contexto.
        """
        # Fazer login no cliente de teste
        self.client.login(username='testuser', password='12345')
        
        # Fazer uma solicitação GET
        response = self.client.get(self.url)
        
        # Verificar se a resposta é 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o template correto foi usado
        self.assertTemplateUsed(response, 'blog/criar.html')
        
        # Verificar se o formulário está presente no contexto
        self.assertIn('form', response.context)

    def test_criar_post_view_post(self):
        """
        Testa a criação de um novo post através de uma solicitação POST válida,
        verificando se o redirecionamento ocorre e se o post é criado corretamente.
        """
        # Fazer login no cliente de teste
        self.client.login(username='testuser', password='12345')
        
        # Dados para enviar no formulário
        data = {
            'titulo': 'Teste de Título',
            'texto': 'Conteúdo do post de teste'
        }
        
        # Fazer uma solicitação POST
        response = self.client.post(self.url, data)
        
        # Verificar se houve redirecionamento após a criação do post
        self.assertEqual(response.status_code, 302)
        
        # Verificar se o redirecionamento foi para a lista de posts
        self.assertRedirects(response, reverse('post_list'))
        
        # Verificar se o post foi criado
        post = Post.objects.get(titulo='Teste de Título')
        self.assertIsNotNone(post)
        self.assertEqual(post.texto, 'Conteúdo do post de teste')
        self.assertEqual(post.autor, self.user)
        self.assertIsNotNone(post.publicado_em)

    def test_criar_post_view_post_invalid(self):
        """
        Testa a resposta da view a uma solicitação POST inválida, 
        verificando se o formulário retorna com erros e se o post não é criado.
        """
        # Fazer login no cliente de teste
        self.client.login(username='testuser', password='12345')
        
        # Dados inválidos (campo 'texto' vazio)
        data = {
            'titulo': 'Teste de Título',
            'texto': ''
        }
        
        # Fazer uma solicitação POST
        response = self.client.post(self.url, data)
        
        # Verificar se a resposta é 200 OK (sem redirecionamento)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está presente no contexto com erros
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        
        # Verificar se o post não foi criado
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(titulo='Teste de Título')

class EditarPostViewTest(TestCase):
    """Test cases for the editar view."""

    def setUp(self):
        """Set up the test environment, including a test client, a test user, and a sample post."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            autor=self.user,
            titulo='Post de Teste',
            texto='Conteúdo do post de teste',
            publicado_em=timezone.now()
        )
        self.url = reverse('editar')

    def test_editar_view_get(self):
        """Test the GET request to the editar view."""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/editar.html')
        self.assertIn('posts', response.context)
        self.assertIn('form', response.context)

    def test_editar_view_post_valid(self):
        """Test the POST request to the editar view with valid data."""
        self.client.login(username='testuser', password='12345')
        data = {
            'post_id': self.post.id,
            'titulo': 'Post de Teste Editado',
            'texto': 'Conteúdo do post de teste editado'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post_list'))
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.titulo, 'Post de Teste Editado')
        self.assertEqual(post.texto, 'Conteúdo do post de teste editado')
        self.assertIsNotNone(post.publicado_em)

    def test_editar_view_post_invalid(self):
        """Test the POST request to the editar view with invalid data."""
        self.client.login(username='testuser', password='12345')
        data = {
            'post_id': self.post.id,
            'titulo': '',
            'texto': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/editar.html')
        self.assertIn('posts', response.context)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_editar_view_post_nonexistent_post(self):
        """Test the POST request to the editar view with a non-existent post ID."""
        self.client.login(username='testuser', password='12345')
        data = {
            'post_id': 999,  # ID that does not exist
            'titulo': 'Post de Teste Editado',
            'texto': 'Conteúdo do post de teste editado'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 404)



class DeletarPostViewTest(TestCase):
    """Test cases for the deletar view."""

    def setUp(self):
        """Set up the test environment, including a test client, a test user, and sample posts."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post1 = Post.objects.create(
            autor=self.user,
            titulo='Post de Teste 1',
            texto='Conteúdo do post de teste 1',
            publicado_em=timezone.now()
        )
        self.post2 = Post.objects.create(
            autor=self.user,
            titulo='Post de Teste 2',
            texto='Conteúdo do post de teste 2',
            publicado_em=timezone.now()
        )
        self.url = reverse('deletar')

    def test_deletar_view_get(self):
        """Test the GET request to the deletar view."""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/deletar.html')
        self.assertIn('posts', response.context)
        self.assertIn('n_posts', response.context)
        self.assertEqual(len(response.context['posts']), 2)
        self.assertEqual(response.context['n_posts'], 2)

    def test_deletar_view_post_valid(self):
        """Test the POST request to the deletar view with valid data."""
        self.client.login(username='testuser', password='12345')
        data = {
            'post_id': self.post1.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post1.id)
        remaining_posts = Post.objects.all()
        self.assertEqual(len(remaining_posts), 1)
        self.assertEqual(remaining_posts[0].titulo, 'Post de Teste 2')

    def test_deletar_view_post_invalid(self):
        """Test the POST request to the deletar view with an invalid post ID."""
        self.client.login(username='testuser', password='12345')
        data = {
            'post_id': 999  # ID that does not exist
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 404)
        remaining_posts = Post.objects.all()
        self.assertEqual(len(remaining_posts), 2)

