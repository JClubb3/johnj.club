from django.utils import timezone

from .models import Article
from johnjclub.settings import SITE_TITLE

def latest_articles(request):
    #pylint: disable=E1101
    latest_articles = Article.objects.all().filter(
        enabled=True,
        publish_date__lte = timezone.now()
    )[:5]
    latest_article = latest_articles[0]

    return {"latest_articles": latest_articles, 
            "latest_article": latest_article}

def site_title(request):
    return {"site_title": SITE_TITLE}