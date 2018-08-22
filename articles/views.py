import datetime

from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpRequest
from django.core.paginator import Paginator

from .models import Article, Author, Series, Tag

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """
    The home page for the site. Pulls the content of the Article name "Welcome".

    The index page is intended to be a modified version of the article detail
    page. It essentially shows only the Article's content and nothing else. 
    It is therefore required that an Article exits with the slug "welcome", and
    it is recommended that this Article has `enabled` set to False so it does
    not appear in the Article lists.
    
    Args:
        request (HttpRequest): The incoming request.
    
    Returns:
        HttpResponse: The response object with the article added to context 
            as `article`.
    """

    #pylint: disable=E1101
    welcome_article = Article.objects.get(slug="welcome")

    return render(request, 
                  'articles/index.html', 
                  context={'article': welcome_article})

class AuthorDetailView(generic.DetailView):
    """
    View for an individual Author.
    """

    model = Author

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds this Author's Articles to context, and paginates them.

        This finds all Articles this Author has published, for which those
        Articles are both enabled and the publish date has passed. The
        QuerySet is then paginated to 7 items per page.
        
        Returns:
            dict: The original context, with the Author's Articles as a
                QuerySet available with the key `author_articles`, paginated
                to 7 items per page.
            **kwargs: Not used here; included because Django requires it.
        """

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
    """
    List view for the Series, paginated to 7 items per page.
    """

    model = Series
    paginate_by = 7


class SeriesDetailView(generic.DetailView):
    """
    Detail view for a single Series.
    """

    model = Series

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds all Articles that should be visible for this Series to context.

        Any Article for which `visible` returns True is filtered in to a new
        QuerySet, available with the key `article_list`.
        
        Returns:
            dict: The context dictionary with available Articles for this
            Series available as `article_list`.
        """

        context = super().get_context_data(**kwargs)
        article_list = self.object.article_set.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )
        paginator = Paginator(article_list, 7)
        page = self.request.GET.get('page')
        context["article_list"] = paginator.get_page(page)
        return context


class TagListView(generic.ListView):
    """
    List view for Tags. Currently not used.
    """

    model = Tag


class TagDetailView(generic.DetailView):
    """
    Detail view for Tags. Currently not used.
    """

    model = Tag


class ArticleListView(generic.ListView):
    """
    List view for Articles, filtered to only visible Articles and paginated.
    """

    #pylint: disable=E1101
    queryset = Article.get_available_articles()
    paginate_by = 7


class ArticleDetailView(generic.DetailView):
    """
    Detail view for a single Article.
    """

    #pylint: disable=E1101
    model = Article
    
    def get_object(self) -> Article:
        """
        Checks if this Article should be visible. Raise 404 if not.
        
        Raises:
            Http404: Raised if the Article is not visible.
        
        Returns:
            Article: The Article to be viewed.
        """

        a = super().get_object()
        if not a.visible():
            raise Http404
        return a