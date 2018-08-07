import datetime

from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.http import Http404
from django.core.paginator import Paginator

from .models import Article, Author, Series, Tag

# Create your views here.
def index(request):
    #pylint: disable=E1101
    welcome_article = Article.objects.get(slug="welcome")

    return render(request, 
                  'articles/index.html', 
                  context={'article': welcome_article})

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_article_list = self.object.article_set.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )
        paginator = Paginator(author_article_list, 7)
        page = self.request.GET.get('page')
        context["author_articles"] = paginator.get_page(page)
        return context


class SeriesListView(generic.ListView):
    model = Series
    paginate_by = 7

class SeriesDetailView(generic.DetailView):
    model = Series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article_list"] = self.object.article_set.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )
        return context


class TagListView(generic.ListView):
    model = Tag


class TagDetailView(generic.DetailView):
    model = Tag


class ArticleListView(generic.ListView):
    #pylint: disable=E1101
    queryset = Article.get_available_articles()
    paginate_by = 7


class ArticleDetailView(generic.DetailView):
    #pylint: disable=E1101
    model = Article
    
    def get_object(self):
        a = super().get_object()
        if not a.visible():
            raise Http404
        return a