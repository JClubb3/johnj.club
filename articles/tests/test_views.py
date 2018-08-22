from django.test import TestCase
from django.urls import reverse
from django.template.exceptions import TemplateDoesNotExist
from mock import patch

from articles.models import Author, Series, Article, Tag
from .test_models import fake_now, fake_later, fake_slightly_later


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        #pylint:disable=E1101
        a = Author.objects.create(
            name = "test author",
            bio = "test"
        )
        s = Series.objects.create(
            name = "test series",
            description = "test"
        )
        Article.objects.create(
            title = "Welcome",
            content = "Test article",
            shortline = "test",
            series = s,
            author = a
        )

    def test_response_code(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_home_article(self):
        #pylint:disable=E1101
        response = self.client.get(reverse("index"))
        expected = Article.objects.get(title="Welcome")
        self.assertEqual(expected, response.context["article"])

    def test_home_article_content(self):
        response = self.client.get(reverse("index"))
        expected = "Test article"
        self.assertContains(response, expected)


class TestAuthorDetailPage(TestCase):

    @classmethod
    @patch("articles.models.timezone.now", fake_now)
    def setUpTestData(cls):
        #pylint: disable=E1101
        s = Series.objects.create(
            name = "test",
            description = "test"
        )
        a = Author.objects.create(
            name = "Test Author",
            bio = "test",
        )
        for x in range(14):
            Article.objects.create(
                title = "Test" + str(x),
                author = a,
                series = s,
                shortline = "test",
                content = "test",
                enabled = bool(not x == 12),
                publish_date = fake_now() if x < 13 else fake_later()
            )

    def test_response_code(self):
        response = self.client.get(reverse("author-detail", args=["test-author"]))
        self.assertEqual(response.status_code, 200)

    def test_url_location(self):
        response = self.client.get("/author/test-author")
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse("author-detail", args=["test-author"]))
        expected = "articles/author_detail.html"
        self.assertTemplateUsed(response, expected)        

    def test_pagination(self):
        response = self.client.get(reverse("author-detail", args=["test-author"]))
        expected = 7
        articles = len(response.context["author_articles"])
        self.assertEqual(expected, articles)

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_pagination_overflow(self):
        response = self.client.get(reverse("author-detail", args=["test-author"]) + "?page=2")
        expected = 5
        articles = len(response.context["author_articles"])
        self.assertEqual(expected, articles)

    def test_article_list_ignores_disabled_articles(self):
        #pylint:disable=E1101
        a = Article.objects.filter(enabled=False)[0]
        response1 = self.client.get(reverse("author-detail", args=["test-author"]))
        response2 = self.client.get(reverse("author-detail", args=["test-author"]) + "?page=2")
        self.assertTrue(a not in response1.context["author_articles"])
        self.assertTrue(a not in response2.context["author_articles"])

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_article_list_ignores_future_articles(self):
        #pylint:disable=E1101
        a = Article.objects.filter(publish_date__gt=fake_slightly_later())[0]
        response1 = self.client.get(reverse("author-detail", args=["test-author"]))
        response2 = self.client.get(reverse("author-detail", args=["test-author"]) + "?page=2")
        self.assertTrue(a not in response1.context["author_articles"])
        self.assertTrue(a not in response2.context["author_articles"])

class TestSeriesListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        #pylint:disable=E1101
        for x in range(10):
            Series.objects.create(
                name = "Series" + str(x),
                description = "test"
            )

    def test_response_code(self):
        response = self.client.get(reverse("series-list"))
        self.assertEqual(response.status_code, 200)

    def test_url_location(self):
        response = self.client.get("/articles/series")
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("series-list"))
        expected = "articles/series_list.html"
        self.assertTemplateUsed(response, expected)

    def test_pagination(self):
        response = self.client.get(reverse("series-list"))
        self.assertTrue(response.context["is_paginated"])

class TestSeriesDetailPage(TestCase):

    @classmethod
    @patch("articles.models.timezone.now", fake_now)
    def setUpTestData(cls):
        #pylint:disable=E1101
        s1 = Series.objects.create(
            name = "Test Series 1",
            description = "test"
        )
        s2 = Series.objects.create(
            name = "Test Series 2",
            description = "test"
        )
        a = Author.objects.create(
            name = "Test Author",
            bio = "test"
        )
        for x in range(12):
            Article.objects.create(
                title = "Test" + str(x),
                series = s1,
                author = a,
                content = "test",
                shortline = "test",
                publish_date = fake_later() if x == 10 else fake_now(),
                enabled = (not x == 11)
            )
        Article.objects.create(
            title = "TestOtherArticle",
            series = s2,
            author = a,
            content = "test",
            shortline = "test"
        )

    def test_response_code(self):
        response = self.client.get(reverse("series-detail", args=["test-series-1"]))
        self.assertEqual(response.status_code, 200)

    def test_url_location(self):
        response = self.client.get("/articles/series/test-series-1")
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("series-detail", args=["test-series-1"]))
        expected = "articles/series_detail.html"
        self.assertTemplateUsed(response, expected)

    def test_pagination(self):
        response = self.client.get(reverse("series-detail", args=["test-series-1"]))
        expected = 7
        articles = len(response.context["article_list"])
        self.assertEqual(articles, expected)

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_pagination_overflow(self):
        response = self.client.get(reverse("series-detail", args=["test-series-1"]) + "?page=2")
        expected = 3
        articles = len(response.context["article_list"])
        self.assertEqual(expected, articles)

    def test_article_list_ignores_disabled_articles(self):
        #pylint:disable=E1101
        a = Article.objects.filter(enabled=False)[0]
        response1 = self.client.get(reverse("series-detail", args=["test-series-1"]))
        response2 = self.client.get(reverse("series-detail", args=["test-series-1"]) + "?page=2")
        self.assertTrue(a not in response1.context["article_list"])
        self.assertTrue(a not in response2.context["article_list"])

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_article_list_ignores_future_articles(self):
        #pylint:disable=E1101
        a = Article.objects.filter(publish_date__gt=fake_slightly_later())[0]
        response1 = self.client.get(reverse("series-detail", args=["test-series-1"]))
        response2 = self.client.get(reverse("series-detail", args=["test-series-1"]) + "?page=2")
        self.assertTrue(a not in response1.context["article_list"])
        self.assertTrue(a not in response2.context["article_list"])

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_article_list_ignores_other_series(self):
        #pylint:disable=E1101
        s = Series.objects.get(name="Test Series 2")
        a = Article.objects.filter(series=s)[0]
        response1 = self.client.get(reverse("series-detail", args=["test-series-1"]))
        response2 = self.client.get(reverse("series-detail", args=["test-series-1"]) + "?page=2")
        self.assertTrue(a not in response1.context["article_list"])
        self.assertTrue(a not in response2.context["article_list"])

class TestTagListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        #pylint:disable=E1101
        Tag.objects.create(name="Test")

    def test_response_code(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get(reverse("tag-list"))

    def test_url_location(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get("/articles/tags")

class TestTagDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        #pylint:disable=E1101
        Tag.objects.create(name="Test")

    def test_response_code(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get(reverse("tag-detail", args=["test"]))

    def test_url_location(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get("/articles/tags/test")


class TestArticleListView(TestCase):

    @classmethod
    @patch("articles.models.timezone.now", fake_now)
    def setUpTestData(cls):
        #pylint:disable=E1101
        a = Author.objects.create(
            name = "Test Author",
            bio = "test"
        )
        s = Series.objects.create(
            name = "Test Series",
            description = "test"
        )
        for x in range(13):
            Article.objects.create(
                title = "Test" + str(x),
                author = a,
                series = s,
                content = "test",
                shortline = "test",
                publish_date = fake_later() if x == 11 else fake_now(),
                enabled = not x == 12
            )

    def test_response_code(self):
        response = self.client.get(reverse("article-list"))
        self.assertEqual(response.status_code, 200)

    def test_url_location(self):
        response = self.client.get("/articles")
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("article-list"))
        expected = "articles/article_list.html"
        self.assertTemplateUsed(response, expected)

    def test_pagination(self):
        response = self.client.get(reverse("article-list"))
        self.assertTrue(response.context["is_paginated"])

    @patch("articles.models.timezone.now", fake_now)
    def test_pagination_overflow(self):
        response = self.client.get(reverse("article-list") + "?page=2")
        expected = 4
        articles = len(response.context["article_list"])
        self.assertEqual(expected, articles)

    def test_article_list_ignores_disabled_articles(self):
        #pylint:disable=E1101
        a = Article.objects.filter(enabled=False)[0]
        response1 = self.client.get(reverse("article-list"))
        response2 = self.client.get(reverse("article-list") + "?page=2")
        self.assertTrue(a not in response1.context["article_list"])
        self.assertTrue(a not in response2.context["article_list"])

    @patch("articles.models.timezone.now", fake_now)
    def test_article_list_ignores_future_articles(self):
        #pylint:disable=E1101
        a = Article.objects.filter(publish_date__gt=fake_slightly_later())[0]
        response1 = self.client.get(reverse("article-list"))
        response2 = self.client.get(reverse("article-list") + "?page=2")
        self.assertTrue(a not in response1.context["article_list"])
        self.assertTrue(a not in response2.context["article_list"])

class TestArticleDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        #pylint:disable=E1101
        a = Author.objects.create(
            name = "Test Author",
            bio = "test"
        )
        s = Series.objects.create(
            name = "Test Series",
            description = "test"
        )
        pub_dates = [fake_now(), fake_later(), fake_now()]
        for index, date in enumerate(pub_dates):
            Article.objects.create(
                title = "Test" + str(index),
                content = "test",
                series = s,
                author = a,
                publish_date = date,
                enabled = bool(index < 2)
            )

    def test_response_code(self):
        response = self.client.get(reverse("article-detail", args=["test-series", "test0"]))
        self.assertEqual(response.status_code, 200)

    def test_url_location(self):
        response = self.client.get("/articles/test-series/test0")
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("article-detail", args=["test-series", "test0"]))
        expected = "articles/article_detail.html"
        self.assertTemplateUsed(response, expected)

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_article_detail_ignores_future_articles(self):
        response = self.client.get(reverse("article-detail", args=["test-series", "test1"]))
        self.assertEqual(response.status_code, 404)

    def test_article_detail_ignores_disabled_articles(self):
        response = self.client.get(reverse("article-detail", args=["test-series", "test2"]))
        self.assertEqual(response.status_code, 404)