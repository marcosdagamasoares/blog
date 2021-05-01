from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.forms import Comentario
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )

        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        # TESTE
        # print(self.kwargs)
        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario  # classe que está em forms.py
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()  # obtém o post que está neste momento.

        # Preciso saber se o comentário está ou não publicado e qual post desses comentários.
        comentarios = Comentario.objects.filter(publicado_comentario=True,
                                                post_comentario=post.id)
        # Injetando o comentário. Cria uma chave dentro do dicionário chamada de
        # (comentarios). Foi injetado este novo contexto.
        contexto['comentarios'] = comentarios

        return contexto

    # validar o formulário, se o formulário for válido, reescrever este método
    def form_valid(self, form):
        # post onde estamos,enquanto não criar cometário e mandar salvar ele vai validar.
        post = self.get_object()
        # Precisa terminar os campos do (cometario) ver no models.py do (comentario).
        # Só estamos pegando 3 campos que são (nome_comentario), (email_comentario) e
        # (comentario), precisa colocar em qual (post) está sendo comentado que é
        # o campo (post_comentario).
        comentario = Comentario(**form.cleaned_data)
        # Após o makemigrations e migrate
        # Colocar qual post que é
        comentario.post_comentario = post
        # checar se o usuário está logado ou não

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentário enviado com sucesso')

        return redirect('post_detalhes', pk=post.id)
