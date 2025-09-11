from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Noticia, Categoria, NoticiaDestaque, BannerNoticias
from django.core.paginator import Paginator
from django.http import HttpResponse
from taggit.models import Tag
from django.db.models import Q
from django.db.models.functions import Lower


class PaginaInicialNoticias(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/pagina_inicial_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 6 

    def get_queryset(self):
        return Noticia.objects.filter(status='PUBLICADO').order_by('-data_atualizacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destaques'] = NoticiaDestaque.objects.all().select_related('noticia')
        context['categorias'] = Categoria.objects.all()
        context['banner'] = BannerNoticias.objects.filter(ativo=True).first()
        return context

class DetalheNoticia(DetailView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/detalhe_noticia.html'
    context_object_name = 'noticia'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Noticia.objects.filter(status='PUBLICADO')

class NoticiasPorCategoria(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/noticias_por_categoria.html'
    context_object_name = 'noticias'
    paginate_by = 9 

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Noticia.objects.filter(categorias=self.categoria, status='PUBLICADO').order_by('-data_publicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context

def mais_noticias_ajax(request):
    """
    View para a paginação 'Carregar Mais' com AJAX.
    """
    page_number = request.GET.get('page', 2) # Começa da página 2
    noticias_list = Noticia.objects.filter(status='PUBLICADO').order_by('-data_publicacao')
    paginator = Paginator(noticias_list, 6)

    try:
        page_number = int(page_number)
        # Se a página pedida não existir, o Paginator levanta uma exceção
        if page_number > paginator.num_pages:
            return HttpResponse('') # Retorna uma resposta vazia
            
        page_obj = paginator.page(page_number)

    except (ValueError, TypeError):
        # Se o número da página não for um inteiro, retorna vazio
        return HttpResponse('')

    return render(request, 'gerenciamento_noticias/html/partials/noticia_card.html', {'noticias': page_obj})

class NoticiasPorTag(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/noticias_por_tag.html'
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Noticia.objects.filter(tags=self.tag, status='PUBLICADO').order_by('-data_publicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
    
class BuscaNoticias(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/busca_resultados.html'
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        # Pega o parâmetro 'q' da URL (ex: /busca/?q=agricultura)
        query = self.request.GET.get('q', '')
        if query:
            # Filtra notícias publicadas que contenham a palavra-chave no título,
            # no subtítulo, no corpo OU no nome de uma tag associada.
            # O .distinct() evita resultados duplicados.
            return Noticia.objects.filter(
                Q(titulo__icontains=query) |
                Q(subtitulo__icontains=query) |
                Q(corpo__icontains=query) |
                Q(tags__name__icontains=query),
                status='PUBLICADO'
            ).distinct().order_by('-data_publicacao')
        
        # Se não houver busca, não retorna nada
        return Noticia.objects.none()

    def get_context_data(self, **kwargs):
        # Adiciona a palavra buscada ao contexto para usá-la no título da página
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context