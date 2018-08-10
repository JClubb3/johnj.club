from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http.request import HttpRequest
from django.conf import settings

from .models import Article, Series

def latest_articles(request: HttpRequest) -> dict:
    """
    Gets the newest five articles and the absolute newest article.
    
    Args:
        request (HttpRequest): The incoming request.

    Returns:
        dict: A dict containing the the latest articles and latest article, 
            available as `latest_articles` and `latest_article`, respectively, 
            if they exist. Otherwise each are empty strings.
    """

    #pylint: disable=E1101
    try:
        latest_articles = Article.get_available_articles()[:5]
        latest_article = latest_articles[0]
    except IndexError:
        latest_articles = ""
        latest_article = ""

    return {"latest_articles": latest_articles, 
            "latest_article": latest_article}

def site_title(request: HttpRequest) -> dict:
    """
    Adds `SITE_TITLE` from settings to context.
    
    Args:
        request (HttpRequest): The incoming request.
    
    Returns:
        dict: A dict containing the The SITE_TITLE, available as `site_title`.
    """

    return {"site_title": settings.SITE_TITLE}

def wyverns_and_whimsy_link(request: HttpRequest) -> dict:
    """
    Adds the link to the `Wyverns and Whimsy` series.

    This, the `about_met_link`, and the `portfolio_link` context processors
    are highly idiomatic to this project. They would probably be better
    implemented as some sort of iterator in settings, and have the nav and
    context processors add them in dynamically. But this works for my use
    case.
    
    Args:
        request (HttpRequest): The incoming request.
    
    Returns:
        dict: A dict containing the URL of the Wyverns and Whimsy link,
            available as `wyverns_link`, if it exists. Otherwise the value is
            an octothorpe.
    """

    #pylint: disable=E1101
    try:
        w = Series.objects.get(name="Wyverns and Whimsy")
    except ObjectDoesNotExist:
        return {"wyverns_link": "#"}
    return {"wyverns_link": w.get_absolute_url()}

def about_me_link(request: HttpRequest) -> dict:
    """
    Adds the link to the "About Me" article.
    
    Args:
        request (HttpRequest): The incoming request.
    
    Returns:
        dict: A dict containing the "About Me" link, available as 
            `about_link`, if it exists. Otherwise an octothorpe.
    """

    #pylint: disable=E1101
    try:
        a = Article.objects.get(title="About Me")
    except ObjectDoesNotExist:
        return {"about_link": "#"}
    return {"about_link": a.get_absolute_url()}

def portfolio_link(request: HttpRequest) -> dict:
    """
    Adds the link to the "Portfolio" article.
    
    Args:
        request (HttpRequest): The incoming request.
    
    Returns:
        dict: A dict containing the "Portfolio" link, available as 
            `portfolio_link`, if it exists. Otherwise an octothorpe.
    """

    #pylint: disable=E1101
    try:
        a = Article.objects.get(title="Portfolio")
    except ObjectDoesNotExist:
        return {"portfolio_link": "#"}
    return {"portfolio_link": a.get_absolute_url()}