from django.test import TestCase, RequestFactory
from django.conf import settings

from articles.context_processors import (latest_articles, site_title, 
    wyverns_and_whimsy_link, about_me_link, portfolio_link)
from articles.models import Series, Author, Article

class TestSiteTitle(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
    
    def test_site_title(self):
        with self.settings(SITE_TITLE="Test Site"):
            request = self.factory.get("/")
            response = site_title(request)
            self.assertEquals("Test Site", response["site_title"])

class TestArticlesContextProcessors(TestCase):

    @classmethod
    def setUpTestData(cls):
        #pylint: disable = E1101
        series = Series.objects.create(
            name = "Wyverns and Whimsy",
            description = "test"
        )
        author = Author.objects.create(
            name = "Test",
            bio = "test"
        )
        to_create = ["About Me", "Portfolio", "Test1", "Test2", "Test3", "Test4"]
        for article in to_create:
            Article.objects.create(
                title = article,
                author = author,
                series = series,
                content = "test",
                shortline = "test"
            )

    def setUp(self):
        self.factory = RequestFactory()

    def test_latest_articles(self):
        request = self.factory.get("/")
        latest = latest_articles(request)
        expected = 5
        self.assertEquals(expected, len(latest["latest_articles"]))

    def test_latest_article_is_most_recent_article(self):
        #pylint: disable=E1101
        request = self.factory.get("/")
        latest = latest_articles(request)
        expected = Article.objects.get(title="Test4")
        self.assertEquals(latest["latest_article"], expected)

    def test_wyverns_and_whimsy_link(self):
        request = self.factory.get("/")
        waw = wyverns_and_whimsy_link(request)
        expected = "/articles/series/wyverns-and-whimsy"
        self.assertEquals(expected, waw["wyverns_link"])

    def test_about_me_link(self):
        request = self.factory.get("/")
        about_me = about_me_link(request)
        expected = "/articles/wyverns-and-whimsy/about-me"
        self.assertEquals(expected, about_me["about_link"])

    def test_portfolio_link(self):
        request = self.factory.get("/")
        portfolio = portfolio_link(request)
        expected = "/articles/wyverns-and-whimsy/portfolio"
        self.assertEquals(expected, portfolio["portfolio_link"])

class TestArticleContextProcessorsNoMatches(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_latest_articles_no_matches(self):
        request = self.factory.get("/")
        latest = latest_articles(request)
        expected = ""
        self.assertEquals(expected, latest["latest_articles"])

    def test_latest_article_no_matches(self):
        request = self.factory.get("/")
        latest = latest_articles(request)
        expected = ""
        self.assertEquals(expected, latest["latest_article"])

    def test_wyverns_and_whimsy_link_no_matches(self):
        request = self.factory.get("/")
        waw = wyverns_and_whimsy_link(request)
        expected = "#"
        self.assertEquals(expected, waw["wyverns_link"])

    def test_about_me_link_no_matches(self):
        request = self.factory.get("/")
        about = about_me_link(request)
        expected = "#"
        self.assertEquals(expected, about["about_link"])

    def test_portfolio_link_no_matches(self):
        request = self.factory.get("/")
        portfolio = portfolio_link(request)
        expected = "#"
        self.assertEquals(expected, portfolio["portfolio_link"])
