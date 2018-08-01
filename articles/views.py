import datetime

from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.db.models import F

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
    paginate_by = 7


class SeriesDetailView(generic.DetailView):
    model = Series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article_list"] = Article.get_available_articles()
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
    queryset = Article.get_available_articles()