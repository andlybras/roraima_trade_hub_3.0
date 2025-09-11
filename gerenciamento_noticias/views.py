from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Noticia, Categoria, NoticiaDestaque
from django.core.paginator import Paginator

class PaginaInicialNoticias(ListView):
    model = Noticia
    template_name = 'gerenciamento_noticias/html/pagina_inicial_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 6 

    def get_queryset(self):
        return Noticia.objects.filter(status='PUBLICADO').order_by('-data_publicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destaques'] = NoticiaDestaque.objects.all().select_related('noticia')
        context['categorias'] = Categoria.objects.all()
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
    page_number = request.GET.get('page', 1)
    noticias_list = Noticia.objects.filter(status='PUBLICADO').order_by('-data_publicacao')
    paginator = Paginator(noticias_list, 6)
    page_obj = paginator.get_page(page_number)
    return render(request, 'gerenciamento_noticias/html/partials/noticia_card.html', {'noticias': page_obj})