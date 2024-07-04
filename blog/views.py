from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Post
from .forms import PostFormCriar


def post_list(request):
    posts = Post.objects.filter(publicado_em__lte=timezone.now()).order_by('-publicado_em')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('painel')
        else:
            return render(request, 'blog/login.html', {'error': 'Usuário ou Senha inválidas'})
    return render(request, 'blog/login.html')

@login_required
def painel_view(request):
    return render(request, 'blog/painel.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def criar_post(request):
    if request.method == 'POST':
        form = PostFormCriar(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.titulo = "titulo do post criado no quill js"
            post.save()
            return HttpResponse(f"Post criado com sucesso: {post.titulo}")
    else:
        form = PostFormCriar()
    return render(request, 'blog/criar.html')

@login_required
def editar(request):
    return render(request, 'blog/editar.html')

@login_required
def deletar(request):
    return render(request, 'blog/deletar.html')