from django.shortcuts import render
from django.views import generic

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


class SeriesListView(generic.ListView):
    model = Series


class SeriesDetailView(generic.DetailView):
    model = Series


class TagListView(generic.ListView):
    model = Tag


class TagDetailView(generic.DetailView):
    model = Tag


class ArticleListView(generic.ListView):
    #pylint: disable=E1101
    queryset = Article.objects.all().filter(enabled=True)
    paginate_by = 7


class ArticleDetailView(generic.DetailView):
    model = Article