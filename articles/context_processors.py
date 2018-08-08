from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Article, Series
from johnjclub.settings import SITE_TITLE

def latest_articles(request):
    #pylint: disable=E1101
    try:
        latest_articles = Article.objects.all().filter(
            enabled=True,
            publish_date__lte = timezone.now()
        )[:5]
        latest_article = latest_articles[0]
    except IndexError:
        latest_articles = ""
        latest_article = ""

    return {"latest_articles": latest_articles, 
            "latest_article": latest_article}

def site_title(request):
    return {"site_title": SITE_TITLE}

def wyverns_and_whimsy_link(request):
    #pylint: disable=E1101
    try:
        w = Series.objects.get(name="Wyverns and Whimsy")
    except ObjectDoesNotExist:
        return {"wyverns_link": "#"}
    return {"wyverns_link": w.get_absolute_url()}

def about_me_link(request):
    #pylint: disable=E1101
    try:
        a = Article.objects.get(title="About Me")
    except ObjectDoesNotExist:
        return {"about_link": "#"}
    return {"about_link": a.get_absolute_url()}

def portfolio_link(request):
    #pylint: disable=E1101
    try:
        a = Article.objects.get(title="Portfolio")
    except ObjectDoesNotExist:
        return {"portfolio_link": "#"}
    return {"portfolio_link": a.get_absolute_url()}