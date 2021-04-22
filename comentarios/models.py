from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=150, verbose_name='Título do Comentário')
    email_comentario = models.EmailField(verbose_name='Email')
    comentario = models.TextField(verbose_name='Comentário')
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE)  #  Tabela Post
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Tabela User
    data_comentario = models.DateTimeField(default=timezone.now)  # Horário atual
    publicado_comentario = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_comentario