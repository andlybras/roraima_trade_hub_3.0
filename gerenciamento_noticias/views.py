from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Noticia, Categoria, NoticiaDestaque, BannerNoticias
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from taggit.models import Tag
from django.db.models import Q, Count
from django.utils import timezone

class PaginaInicialNoticias(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/pagina_inicial_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 6

    def get_queryset(self):

        return Noticia.publicadas.all().order_by('-data_publicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['destaques'] = NoticiaDestaque.objects.filter(
            noticia__in=Noticia.publicadas.all()
        ).select_related('noticia')
        context['categorias'] = Categoria.objects.all()
        context['banner'] = BannerNoticias.objects.filter(ativo=True).first()
        return context

class DetalheNoticia(DetailView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/detalhe_noticia.html'
    context_object_name = 'noticia'
    slug_url_kwarg = 'slug'

    def get_queryset(self):

        return Noticia.publicadas.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        noticia_atual = self.get_object()
        tags_da_noticia = noticia_atual.tags.values_list('id', flat=True)
        materias_relacionadas = Noticia.objects.none()
        if tags_da_noticia:

            materias_relacionadas = Noticia.publicadas.filter(
                tags__in=tags_da_noticia
            ).exclude(id=noticia_atual.id)
            materias_relacionadas = materias_relacionadas.annotate(
                num_common_tags=Count('tags')
            ).order_by('-num_common_tags', '-data_publicacao').distinct()[:4]
        context['materias_relacionadas'] = materias_relacionadas
        return context

class NoticiasPorAutor(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/noticias_por_autor.html' 
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        self.autor = get_object_or_404(User, username=self.kwargs['username'])

        return Noticia.publicadas.filter(autor=self.autor).order_by('-data_publicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor'] = self.autor
        return context

class NoticiasPorCategoria(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/noticias_por_categoria.html'
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])

        return Noticia.publicadas.filter(categorias=self.categoria).order_by('-data_publicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context

def mais_noticias_ajax(request):
    page_number = request.GET.get('page', 2)

    noticias_list = Noticia.publicadas.all().order_by('-data_publicacao')
    paginator = Paginator(noticias_list, 6)
    
    try:
        page_number = int(page_number)
        if page_number > paginator.num_pages:
            return HttpResponse("") 
        page_obj = paginator.page(page_number)
    except (ValueError, TypeError):
        return HttpResponse("")

    return render(request, 'gerenciamento_noticias/html/partials/noticia_card.html', {'noticias': page_obj})

class NoticiasPorTag(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/noticias_por_tag.html'
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Noticia.publicadas.filter(tags=self.tag).order_by('-data_publicacao')
    
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
        query = self.request.GET.get('q', "")
        if query:
            return Noticia.publicadas.filter(
                Q(titulo__icontains=query) |
                Q(subtitulo__icontains=query) |
                Q(corpo__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-data_publicacao')
        return Noticia.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', "")
        return context