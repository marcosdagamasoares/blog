from django.contrib import admin
from .models import Post
# from django_summernote.admin import SummernoteModelAdmin
#
#
class PostAdmin(admin.ModelAdmin):  # admin.ModelAdmin
      list_display = ('id', 'titulo_post', 'autor_post', 'imagem_post', 'data_post', 'categoria_post', 'publicado_post',)
      list_editable = ('publicado_post',)
      list_display_links = ('id', 'titulo_post',)
#     summernote_fields = ('conteudo_post',)

admin.site.register(Post, PostAdmin)


