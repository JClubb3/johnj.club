import pytz

from django.test import TestCase, TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from PIL import Image
from datetime import datetime, timedelta
from mock import patch

from articles.models import Author, Series, Tag, Article

IMAGE_PATH = "articles/tests/test_image.jpg"

TZ = pytz.timezone("America/New_York")
UTC = pytz.timezone("UTC")

def get_test_image() -> SimpleUploadedFile:
    """
    Mocks an image for uploading without actually uploading.
    
    Returns:
        SimpleUploadedFile: The test image, ready to be worked it but
            not uploaded anywhere.
    """

    return SimpleUploadedFile(
        name = "test_image.jpg",
        content = open(IMAGE_PATH, "rb").read(),
        content_type = "image/jpeg"
    )

def fake_now():
    return datetime(2018, 8, 16, 16, 30, 0, 0, tzinfo=TZ)

def fake_slightly_later():
    return fake_now() + timedelta(hours=10)

def fake_later():
    return fake_now() + timedelta(days=1)

def fake_later_utc():
    return fake_later().astimezone(UTC)

class TestModelAuthor(TestCase):
    #pylint: disable=E1101

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(
            name = "Test Author",
            bio = "This Author doesn't exist!",
            image_raw = get_test_image()
        )

    def test_name_label(self):
        a = Author.objects.all()[0]
        name_label = a._meta.get_field("name").verbose_name
        expected = "name"
        self.assertEquals(name_label, expected)

    def test_name_unique(self):
        a = Author.objects.all()[0]
        name_unique = a._meta.get_field("name").unique
        self.assertTrue(name_unique)

    def test_bio_label(self):
        a = Author.objects.all()[0]
        bio_label = a._meta.get_field("bio").verbose_name
        expected = "bio"
        self.assertEquals(bio_label, expected)

    def test_bio_help_text(self):
        a = Author.objects.all()[0]
        help_text = a._meta.get_field("bio").help_text
        expected = "I mean. It's a bio."
        self.assertEquals(help_text, expected)

    def test_image_raw_label(self):
        a = Author.objects.all()[0]
        image_label = a._meta.get_field("image_raw").verbose_name
        expected = "image raw"
        self.assertEquals(image_label, expected)

    def test_image_raw_blank(self):
        a = Author.objects.all()[0]
        blank = a._meta.get_field("image_raw").blank
        self.assertTrue(blank)

    def test_image_raw_upload_to(self):
        a = Author.objects.all()[0]
        upload_to = a._meta.get_field("image_raw").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_raw_help_text(self):
        a = Author.objects.all()[0]
        expected = "A base image that will be manipulated to generate other image fields."
        help_text = a._meta.get_field("image_raw").help_text
        self.assertEquals(help_text, expected)

    def test_image_raw_size_unchanged(self):
        a = Author.objects.all()[0]
        test_image = Image.open(IMAGE_PATH)
        image_raw = Image.open(a.image_raw)
        self.assertEquals(test_image.size, image_raw.size)

    def test_image_thumbnail_label(self):
        a = Author.objects.all()[0]
        label = a._meta.get_field("image_thumbnail").verbose_name
        expected = "image thumbnail"
        self.assertEquals(label, expected)

    def test_image_thumbnail_blank(self):
        a = Author.objects.all()[0]
        blank = a._meta.get_field("image_thumbnail").blank
        self.assertTrue(blank)

    def test_image_thumbnail_null(self):
        a = Author.objects.all()[0]
        null = a._meta.get_field("image_thumbnail").null
        self.assertTrue(null)

    def test_image_thumbnail_upload_to(self):
        a = Author.objects.all()[0]
        upload_to = a._meta.get_field("image_thumbnail").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_thumbnail_help_text(self):
        a = Author.objects.all()[0]
        help_text = a._meta.get_field("image_thumbnail").help_text
        expected = "A smaller version of the base image. Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)

    def test_image_thumbnail_maximum_size(self):
        a = Author.objects.all()[0]
        size = Image.open(a.image_thumbnail).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(size <= expected)

    def test_image_thumbnail_at_least_one_dimension_is_maxed(self):
        a = Author.objects.all()[0]
        size = Image.open(a.image_thumbnail).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_thumbnail_file_type(self):
        a = Author.objects.all()[0]
        image_format = Image.open(a.image_thumbnail).format
        expected = "PNG"
        self.assertEquals(image_format, expected)

    def test_image_thumbnail_name(self):
        a = Author.objects.all()[0]
        name = a.image_thumbnail.name
        expected = "uploads/test_image_thumbnail.png"
        self.assertEquals(name, expected)

    def test_image_thumbnail_transparent_label(self):
        a = Author.objects.all()[0]
        label = a._meta.get_field("image_thumbnail_transparent").verbose_name
        expected = "image thumbnail transparent"
        self.assertEquals(label, expected)

    def test_image_thumbnail_transparent_blank(self):
        a = Author.objects.all()[0]
        blank = a._meta.get_field("image_thumbnail_transparent").blank
        self.assertTrue(blank)

    def test_image_thumbnail_transparent_null(self):
        a = Author.objects.all()[0]
        null = a._meta.get_field("image_thumbnail_transparent").null
        self.assertTrue(null)

    def test_image_thumbnail_transparent_upload_to(self):
        a = Author.objects.all()[0]
        upload_to = a._meta.get_field("image_thumbnail_transparent").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_thumbnail_transparent_help_text(self):
        a = Author.objects.all()[0]
        help_text = a._meta.get_field("image_thumbnail_transparent").help_text
        expected = "A smaller version of the base image, with an alpha layer. Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)

    def test_image_thumbnail_transparent_maximum_size(self):
        a = Author.objects.all()[0]
        size = Image.open(a.image_thumbnail_transparent).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(size <= expected)

    def test_image_thumbnail_transparent_at_least_one_dimension_is_maxed(self):
        a = Author.objects.all()[0]
        size = Image.open(a.image_thumbnail_transparent).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_thumbnail_transparent_file_type(self):
        a = Author.objects.all()[0]
        image_format = Image.open(a.image_thumbnail_transparent).format
        expected = "PNG"
        self.assertEquals(image_format, expected)
    
    def test_image_thumbnail_transparent_has_alpha(self):
        a = Author.objects.all()[0]
        image_transparent = Image.open(a.image_thumbnail_transparent).getchannel("A")
        self.assertTrue(image_transparent)

    def test_image_thumbnail_transparent_name(self):
        a = Author.objects.all()[0]
        name = a.image_thumbnail_transparent.name
        expected = "uploads/test_image_thumbnail_transparent.png"
        self.assertEquals(name, expected)

    def test_image_full_label(self):
        a = Author.objects.all()[0]
        label = a._meta.get_field("image_full").verbose_name
        expected = "image full"
        self.assertEquals(label, expected)

    def test_image_full_blank(self):
        a = Author.objects.all()[0]
        blank = a._meta.get_field("image_full").blank
        self.assertTrue(blank)

    def test_image_full_null(self):
        a = Author.objects.all()[0]
        null = a._meta.get_field("image_full").null
        self.assertTrue(null)

    def test_image_full_upload_to(self):
        a = Author.objects.all()[0]
        upload_to = a._meta.get_field("image_full").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_full_help_text(self):
        a = Author.objects.all()[0]
        help_text = a._meta.get_field("image_full").help_text
        expected = "A good-sized version of the base image. Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)
    
    def test_image_full_maximum_size(self):
        a = Author.objects.all()[0]
        size = Image.open(a.image_full).size
        expected = settings.IMAGE_FULL_SIZE
        self.assertTrue(size <= expected)

    def test_image_full_at_least_one_dimension_is_maxed(self):
        a = Author.objects.all()[0]
        size = Image.open(a.image_full).size
        expected = settings.IMAGE_FULL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_full_file_type(self):
        a = Author.objects.all()[0]
        image_format = Image.open(a.image_full).format
        expected = "PNG"
        self.assertEquals(image_format, expected)

    def test_image_full_name(self):
        a = Author.objects.all()[0]
        name = a.image_full.name
        expected = "uploads/test_image_full.png"
        self.assertEquals(name, expected)

    def test_slug_label(self):
        a = Author.objects.all()[0]
        label = a._meta.get_field("slug").verbose_name
        expected = "slug"
        self.assertEquals(label, expected)

    def test_slug_help_text(self):
        a = Author.objects.all()[0]
        help_text = a._meta.get_field("slug").help_text
        expected = "A no space name to be used for URLs"
        self.assertEquals(help_text, expected)

    def test_slug_blank(self):
        a = Author.objects.all()[0]
        blank = a._meta.get_field("slug").blank
        self.assertTrue(blank)

    def test_slug_null(self):
        a = Author.objects.all()[0]
        null = a._meta.get_field("slug").null
        self.assertTrue(null)

    def test_slug_editable(self):
        a = Author.objects.all()[0]
        editable = a._meta.get_field("slug").editable
        self.assertFalse(editable)

    def test_slug_is_slugified_name(self):
        a = Author.objects.all()[0]
        slug = a.slug
        expected = "test-author"
        self.assertEquals(slug, expected)

    def test_slug_does_not_change_when_name_is_changed(self):
        a = Author.objects.all()[0]
        expected = "test-author"
        a.name = "New Name"
        a.save()
        a.refresh_from_db()
        self.assertEquals(a.slug, expected)

    def test_author_str_is_name(self):
        a = Author.objects.all()[0]
        expected = "Test Author"
        self.assertEquals(str(a), expected)

    def test_get_absolute_url(self):
        a = Author.objects.all()[0]
        expected = "/author/test-author"
        url = a.get_absolute_url()
        self.assertEquals(expected, url)
        

class TestModelSeries(TestCase):
    #pylint: disable=E1101

    @classmethod
    def setUpTestData(cls):
        Series.objects.create(
            name = "Test Series",
            description = "A series for tests and stuff",
            image_raw = get_test_image()
        )

    def test_name_label(self):
        s = Series.objects.all()[0]
        label = s._meta.get_field("name").verbose_name
        expected = "name"
        self.assertEquals(label, expected)

    def test_name_max_length(self):
        s = Series.objects.all()[0]
        max_length = s._meta.get_field("name").max_length
        expected = 40
        self.assertEquals(max_length, expected)
    
    def test_name_help_text(self):
        s = Series.objects.all()[0]
        help_text = s._meta.get_field("name").help_text
        expected = "The series this article should be filed under; will be used for URLs"
        self.assertEquals(help_text, expected)

    def test_name_unique(self):
        s = Series.objects.all()[0]
        unique = s._meta.get_field("name").unique
        self.assertTrue(unique)

    def test_description_label(self):
        s = Series.objects.all()[0]
        label = s._meta.get_field("description").verbose_name
        expected = "description"
        self.assertEquals(label, expected)

    def test_description_help_text(self):
        s = Series.objects.all()[0]
        help_text = s._meta.get_field("description").help_text
        expected = "A short description of the series"
        self.assertEquals(help_text, expected)

    def test_description_default_is_blank_string(self):
        s = Series.objects.create(
            name = "Default test"
        )
        self.assertTrue(s.description is "")

    def test_slug_label(self):
        s = Series.objects.all()[0]
        label = s._meta.get_field("slug").verbose_name
        expected = "slug"
        self.assertEquals(label, expected)

    def test_slug_help_text(self):
        s = Series.objects.all()[0]
        help_text = s._meta.get_field("slug").help_text
        expected = "The short version of the name to use in URLs"
        self.assertEquals(help_text, expected)

    def test_slug_null(self):
        s = Series.objects.all()[0]
        null = s._meta.get_field("slug").null
        self.assertTrue(null)

    def test_slug_editable(self):
        s = Series.objects.all()[0]
        editable = s._meta.get_field("slug").editable
        self.assertFalse(editable)

    def test_slug_blank(self):
        s = Series.objects.all()[0]
        blank = s._meta.get_field("slug").blank
        self.assertTrue(blank)

    def test_slug_is_slugified_name(self):
        s = Series.objects.all()[0]
        slug = s.slug
        expected = "test-series"
        self.assertEquals(slug, expected)

    def test_image_raw_label(self):
        a = Series.objects.all()[0]
        image_label = a._meta.get_field("image_raw").verbose_name
        expected = "image raw"
        self.assertEquals(image_label, expected)

    def test_image_raw_blank(self):
        a = Series.objects.all()[0]
        blank = a._meta.get_field("image_raw").blank
        self.assertTrue(blank)

    def test_image_raw_upload_to(self):
        a = Series.objects.all()[0]
        upload_to = a._meta.get_field("image_raw").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_raw_help_text(self):
        a = Series.objects.all()[0]
        expected = "A base image that will be manipulated to generate other image fields."
        help_text = a._meta.get_field("image_raw").help_text
        self.assertEquals(help_text, expected)

    def test_image_raw_size_unchanged(self):
        a = Series.objects.all()[0]
        test_image = Image.open(IMAGE_PATH)
        image_raw = Image.open(a.image_raw)
        self.assertEquals(test_image.size, image_raw.size)

    def test_image_thumbnail_label(self):
        a = Series.objects.all()[0]
        label = a._meta.get_field("image_thumbnail").verbose_name
        expected = "image thumbnail"
        self.assertEquals(label, expected)

    def test_image_thumbnail_blank(self):
        a = Series.objects.all()[0]
        blank = a._meta.get_field("image_thumbnail").blank
        self.assertTrue(blank)

    def test_image_thumbnail_null(self):
        a = Series.objects.all()[0]
        null = a._meta.get_field("image_thumbnail").null
        self.assertTrue(null)

    def test_image_thumbnail_upload_to(self):
        a = Series.objects.all()[0]
        upload_to = a._meta.get_field("image_thumbnail").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_thumbnail_help_text(self):
        a = Series.objects.all()[0]
        help_text = a._meta.get_field("image_thumbnail").help_text
        expected = "A smaller version of the base image. Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)

    def test_image_thumbnail_maximum_size(self):
        a = Series.objects.all()[0]
        size = Image.open(a.image_thumbnail).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(size <= expected)

    def test_image_thumbnail_at_least_one_dimension_is_maxed(self):
        a = Series.objects.all()[0]
        size = Image.open(a.image_thumbnail).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_thumbnail_file_type(self):
        a = Series.objects.all()[0]
        image_format = Image.open(a.image_thumbnail).format
        expected = "PNG"
        self.assertEquals(image_format, expected)

    def test_image_thumbnail_name(self):
        a = Series.objects.all()[0]
        name = a.image_thumbnail.name
        expected = "uploads/test_image_thumbnail.png"
        self.assertEquals(name, expected)

    def test_image_thumbnail_transparent_label(self):
        a = Series.objects.all()[0]
        label = a._meta.get_field("image_thumbnail_transparent").verbose_name
        expected = "image thumbnail transparent"
        self.assertEquals(label, expected)

    def test_image_thumbnail_transparent_blank(self):
        a = Series.objects.all()[0]
        blank = a._meta.get_field("image_thumbnail_transparent").blank
        self.assertTrue(blank)

    def test_image_thumbnail_transparent_null(self):
        a = Series.objects.all()[0]
        null = a._meta.get_field("image_thumbnail_transparent").null
        self.assertTrue(null)

    def test_image_thumbnail_transparent_upload_to(self):
        a = Series.objects.all()[0]
        upload_to = a._meta.get_field("image_thumbnail_transparent").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_thumbnail_transparent_help_text(self):
        a = Series.objects.all()[0]
        help_text = a._meta.get_field("image_thumbnail_transparent").help_text
        expected = "A smaller version of the base image, with an alpha layer. Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)

    def test_image_thumbnail_transparent_maximum_size(self):
        a = Series.objects.all()[0]
        size = Image.open(a.image_thumbnail_transparent).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(size <= expected)

    def test_image_thumbnail_transparent_at_least_one_dimension_is_maxed(self):
        a = Series.objects.all()[0]
        size = Image.open(a.image_thumbnail_transparent).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_thumbnail_transparent_file_type(self):
        a = Series.objects.all()[0]
        image_format = Image.open(a.image_thumbnail_transparent).format
        expected = "PNG"
        self.assertEquals(image_format, expected)
    
    def test_image_thumbnail_transparent_has_alpha(self):
        a = Series.objects.all()[0]
        image_transparent = Image.open(a.image_thumbnail_transparent).getchannel("A")
        self.assertTrue(image_transparent)

    def test_image_thumbnail_transparent_name(self):
        a = Series.objects.all()[0]
        name = a.image_thumbnail_transparent.name
        expected = "uploads/test_image_thumbnail_transparent.png"
        self.assertEquals(name, expected)

    def test_image_full_label(self):
        a = Series.objects.all()[0]
        label = a._meta.get_field("image_full").verbose_name
        expected = "image full"
        self.assertEquals(label, expected)

    def test_image_full_blank(self):
        a = Series.objects.all()[0]
        blank = a._meta.get_field("image_full").blank
        self.assertTrue(blank)

    def test_image_full_null(self):
        a = Series.objects.all()[0]
        null = a._meta.get_field("image_full").null
        self.assertTrue(null)

    def test_image_full_upload_to(self):
        a = Series.objects.all()[0]
        upload_to = a._meta.get_field("image_full").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_full_help_text(self):
        a = Series.objects.all()[0]
        help_text = a._meta.get_field("image_full").help_text
        expected = "A good-sized version of the base image. Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)
    
    def test_image_full_maximum_size(self):
        a = Series.objects.all()[0]
        size = Image.open(a.image_full).size
        expected = settings.IMAGE_FULL_SIZE
        self.assertTrue(size <= expected)

    def test_image_full_at_least_one_dimension_is_maxed(self):
        a = Series.objects.all()[0]
        size = Image.open(a.image_full).size
        expected = settings.IMAGE_FULL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_full_file_type(self):
        a = Series.objects.all()[0]
        image_format = Image.open(a.image_full).format
        expected = "PNG"
        self.assertEquals(image_format, expected)

    def test_image_full_name(self):
        a = Series.objects.all()[0]
        name = a.image_full.name
        expected = "uploads/test_image_full.png"
        self.assertEquals(name, expected)

    def test_latest_article_date_label(self):
        a = Series.objects.all()[0]
        label = a._meta.get_field("latest_article_date").verbose_name
        expected = "latest article date"
        self.assertEquals(label, expected)

    def test_latest_article_date_null(self):
        a = Series.objects.all()[0]
        null = a._meta.get_field("latest_article_date").null
        self.assertTrue(null)

    def test_latest_article_date_blank(self):
        a = Series.objects.all()[0]
        blank = a._meta.get_field("latest_article_date").blank
        self.assertTrue(blank)

    def test_latest_article_date_help_text(self):
        a = Series.objects.all()[0]
        help_text = a._meta.get_field("latest_article_date").help_text
        expected = "The date and time the newest Article of this Series was published. Will be set automatically when an Article is created."
        self.assertEquals(help_text, expected)

    def test_series_str_is_name(self):
        a = Series.objects.all()[0]
        expected = "Test Series"
        self.assertEquals(str(a), expected)

    def test_series_absolute_url(self):
        a = Series.objects.all()[0]
        expected = "/articles/series/test-series"
        url = a.get_absolute_url()
        self.assertEquals(expected, url)

    def test_latest_list_is_empty_if_no_articles(self):
        a = Series.objects.all()[0]
        self.assertIsNone(a.latest_list())

    def test_latest_list_returns_five_articles(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(5):
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a
            )
        articles = Article.objects.all()
        self.assertEquals(list(articles), a.latest_list())

    def test_latest_list_ignores_disabled_articles(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(10):
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a,
                enabled = bool(x % 2)
            )
        expected = list(Article.objects.filter(enabled=True))
        articles = a.latest_list()
        self.assertEquals(expected, articles)

    @patch("articles.models.timezone.now", fake_now)
    def test_latest_list_ignores_future_articles(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(10):
            if x % 2:
                pub_date = fake_now() - timedelta(minutes=(10 - x))
            else:
                pub_date = fake_later() + timedelta(minutes=(10 - x))
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a,
                publish_date = pub_date
            )
        expected = list(Article.objects.filter(
            publish_date__lte = (fake_now() + timedelta(hours=1))
        ))
        articles = a.latest_list()
        self.assertEquals(expected, articles)

    @patch("articles.models.timezone.now", fake_now)
    def test_latest_list_gets_only_five_articles(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(10):
            pub_date = fake_now() - timedelta(minutes=(10 - x))
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a,
                publish_date = pub_date
            )
        expected = 5
        articles = len(a.latest_list())
        self.assertEquals(expected, articles)

    @patch("articles.models.timezone.now", fake_now)
    def test_latest_article_returns_latest_article(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(2):
            pub_date = fake_now() - timedelta(minutes=(10-x))
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a,
                publish_date = pub_date
            )
        expected = Article.objects.get(title="Test1")
        article = a.latest_article()
        self.assertEquals(expected, article)
    
    @patch("articles.models.timezone.now", fake_now)
    def test_latest_article_ignores_disabled_articles(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(2):
            pub_date = fake_now() - timedelta(minutes=(10-x))
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a,
                publish_date = pub_date,
                enabled = bool(x % 2)
            )
        expected = Article.objects.get(title="Test1")
        article = a.latest_article()
        self.assertEquals(article, expected)

    @patch("articles.models.timezone.now", fake_now)
    def test_latest_article_returns_none_with_no_articles(self):
        a = Series.objects.all()[0]
        article = a.latest_article()
        self.assertIsNone(article)

    @patch("articles.models.timezone.now", fake_now)
    def test_latest_article_ignores_future_articles(self):
        author = Author.objects.create(name="Test", bio="test")
        a = Series.objects.all()[0]
        for x in range(2):
            if x % 2:
                pub_date = fake_now() - timedelta(minutes=1)
            else:
                pub_date = fake_later()
            Article.objects.create(
                title = "Test" + str(x),
                content = "test content",
                shortline = "test article",
                author = author,
                series = a,
                publish_date = pub_date,
            )
        expected = Article.objects.get(title="Test1")
        article = a.latest_article()
        self.assertEquals(article, expected)

            
class TestModelTag(TestCase):
    #pylint: disable=E1101

    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name = "Test Tag")

    def test_name_label(self):
        a = Tag.objects.all()[0]
        label = a._meta.get_field("name").verbose_name
        expected = "name"
        self.assertEquals(label, expected)

    def test_name_max_length(self):
        a = Tag.objects.all()[0]
        max_length = a._meta.get_field("name").max_length
        expected = 200
        self.assertEquals(max_length, expected)

    def test_name_unique(self):
        a = Tag.objects.all()[0]
        unique = a._meta.get_field("name").unique
        self.assertTrue(unique)

    def test_slug_blank(self):
        a = Tag.objects.all()[0]
        blank = a._meta.get_field("slug").blank
        self.assertTrue(blank)

    def test_slug_editable(self):
        a = Tag.objects.all()[0]
        editable = a._meta.get_field("slug").editable
        self.assertFalse(editable)

    def test_tag_str_is_name(self):
        a = Tag.objects.all()[0]
        expected = "Test Tag"
        self.assertEquals(str(a), expected)

    def test_tag_slug_is_slugified_name(self):
        a = Tag.objects.all()[0]
        expected = "test-tag"
        slug = a.slug
        self.assertEquals(expected, slug)

    def test_absolute_url(self):
        a = Tag.objects.all()[0]
        expected = "/articles/tags/test-tag"
        url = a.get_absolute_url()
        self.assertEquals(url, expected)

class TestModelArticle(TestCase):
    #pylint: disable = E1101

    @classmethod
    @patch("articles.models.timezone.now", fake_now)
    @patch("django.utils.timezone.now", fake_now)
    def setUpTestData(cls):
        author = Author.objects.create(name="Test", bio="test")
        series = Series.objects.create(
            name = "Test Series", 
            description = "test"
        )
        Article.objects.create(
            title = "Test Article",
            content = "This is a test article",
            shortline = "for testing",
            author = author,
            series = series,
            image_raw = get_test_image()
        )

    def test_title_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("title").verbose_name
        expected = "title"
        self.assertEquals(label, expected)

    def test_title_max_length(self):
        a = Article.objects.all()[0]
        max_length = a._meta.get_field("title").max_length
        expected = 200
        self.assertEquals(max_length, expected)

    def test_title_unique(self):
        a = Article.objects.all()[0]
        unique = a._meta.get_field("title").unique
        self.assertTrue(unique)

    def test_slug_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("slug").verbose_name
        expected = "slug"
        self.assertEquals(label, expected)

    def test_slug_help_text(self):
        a = Article.objects.all()[0]
        help_text = a._meta.get_field("slug").help_text
        expected = "Slugs are short versions of the title used for URLs"
        self.assertEquals(help_text, expected)

    def test_slug_blank(self):
        a = Article.objects.all()[0]
        blank = a._meta.get_field("slug").blank
        self.assertTrue(blank)

    def test_slug_null(self):
        a = Article.objects.all()[0]
        null = a._meta.get_field("slug").null
        self.assertTrue(null)

    def test_slug_editable(self):
        a = Article.objects.all()[0]
        editable = a._meta.get_field("slug").editable
        self.assertFalse(editable)

    def test_content_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("content").verbose_name
        expected = "content"
        self.assertEquals(label, expected)

    def test_content_help_text(self):
        a = Article.objects.all()[0]
        help_text = a._meta.get_field("content").help_text
        expected = "Unlimited length. HTML formatted."
        self.assertEquals(help_text, expected)

    def test_shortline_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("shortline").verbose_name
        expected = "shortline"
        self.assertEquals(label, expected)

    def test_shortline_max_length(self):
        a = Article.objects.all()[0]
        max_length = a._meta.get_field("shortline").max_length
        expected = 200
        self.assertEquals(max_length, expected)

    def test_shortline_help_text(self):
        a = Article.objects.all()[0]
        help_text = a._meta.get_field("shortline").help_text
        expected = "A short summary to show in the sidebar and under the article title"
        self.assertEquals(help_text, expected)

    def test_author_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("author").verbose_name
        expected = "author"
        self.assertEquals(label, expected)

    def test_author_null(self):
        a = Article.objects.all()[0]
        null = a._meta.get_field("author").null
        self.assertTrue(null)

    def test_author_on_delete(self):
        Author.objects.all()[0].delete()
        a = Article.objects.all()[0]
        author = a.author
        self.assertIsNone(author)

    def test_publish_date_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("publish_date").verbose_name
        expected = "publish date"
        self.assertEquals(label, expected)

    def test_publish_date_default(self):
        a = Article.objects.all()[0]
        pub_date = a.publish_date
        expected = fake_now()
        self.assertEquals(pub_date, expected)

    def test_date_modified_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("date_modified").verbose_name
        expected = "date modified"
        self.assertEquals(label, expected)

    def test_date_modified_editable(self):
        a = Article.objects.all()[0]
        editable = a._meta.get_field("date_modified").editable
        self.assertFalse(editable)

    @patch("articles.models.timezone.now", fake_later_utc)
    def test_date_modified_updates_automatically(self):
        a = Article.objects.all()[0]
        a.title = "New Title"
        a.save()
        a.refresh_from_db()
        expected = fake_later_utc()
        date = a.date_modified
        self.assertEquals(date, expected)

    def test_date_created_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("date_created").verbose_name
        expected = "date created"
        self.assertEquals(label, expected)

    def test_date_created_editable(self):
        a = Article.objects.all()[0]
        editable = a._meta.get_field("date_created").editable
        self.assertFalse(editable)

    def test_series_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("series").verbose_name
        expected = "series"
        self.assertEquals(label, expected)

    def test_series_default(self):
        s2 = Series.objects.create(
            name = "new series",
            description = "new series"    
        )
        author = Author.objects.all()[0]
        a = Article.objects.create(
            title = "Test Article2",
            content = "This is a test article2",
            shortline = "for testing",
            author = author,
        )
        series = a.series
        self.assertEquals(series, s2)

    def test_series_on_delete(self):
        s = Series.objects.all()[0]
        s2 = Series.objects.create(
            name = "test series",
            description = "test series"
        )
        s.delete()
        a = Article.objects.all()[0]
        series = a.series
        self.assertEquals(series, s2)

    def test_tag_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("tags").verbose_name
        expected = "tags"
        self.assertEquals(label, expected)
    
    def test_image_raw_label(self):
        a = Article.objects.all()[0]
        image_label = a._meta.get_field("image_raw").verbose_name
        expected = "image raw"
        self.assertEquals(image_label, expected)

    def test_image_raw_blank(self):
        a = Article.objects.all()[0]
        blank = a._meta.get_field("image_raw").blank
        self.assertTrue(blank)

    def test_image_raw_upload_to(self):
        a = Article.objects.all()[0]
        upload_to = a._meta.get_field("image_raw").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_raw_help_text(self):
        a = Article.objects.all()[0]
        expected = "A base image that will be manipulated to generate other image fields."
        help_text = a._meta.get_field("image_raw").help_text
        self.assertEquals(help_text, expected)

    def test_image_raw_size_unchanged(self):
        a = Article.objects.all()[0]
        test_image = Image.open(IMAGE_PATH)
        image_raw = Image.open(a.image_raw)
        self.assertEquals(test_image.size, image_raw.size)

    def test_image_thumbnail_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("image_thumbnail").verbose_name
        expected = "image thumbnail"
        self.assertEquals(label, expected)

    def test_image_thumbnail_blank(self):
        a = Article.objects.all()[0]
        blank = a._meta.get_field("image_thumbnail").blank
        self.assertTrue(blank)

    def test_image_thumbnail_null(self):
        a = Article.objects.all()[0]
        null = a._meta.get_field("image_thumbnail").null
        self.assertTrue(null)

    def test_image_thumbnail_upload_to(self):
        a = Article.objects.all()[0]
        upload_to = a._meta.get_field("image_thumbnail").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_thumbnail_help_text(self):
        a = Article.objects.all()[0]
        help_text = a._meta.get_field("image_thumbnail").help_text
        expected = "Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)

    def test_image_thumbnail_maximum_size(self):
        a = Article.objects.all()[0]
        size = Image.open(a.image_thumbnail).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(size <= expected)

    def test_image_thumbnail_at_least_one_dimension_is_maxed(self):
        a = Article.objects.all()[0]
        size = Image.open(a.image_thumbnail).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_thumbnail_file_type(self):
        a = Article.objects.all()[0]
        image_format = Image.open(a.image_thumbnail).format
        expected = "PNG"
        self.assertEquals(image_format, expected)

    def test_image_thumbnail_name(self):
        a = Article.objects.all()[0]
        name = a.image_thumbnail.name
        expected = "uploads/test_image_thumbnail.png"
        self.assertEquals(name, expected)

    def test_image_thumbnail_transparent_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("image_thumbnail_transparent").verbose_name
        expected = "image thumbnail transparent"
        self.assertEquals(label, expected)

    def test_image_thumbnail_transparent_blank(self):
        a = Article.objects.all()[0]
        blank = a._meta.get_field("image_thumbnail_transparent").blank
        self.assertTrue(blank)

    def test_image_thumbnail_transparent_null(self):
        a = Article.objects.all()[0]
        null = a._meta.get_field("image_thumbnail_transparent").null
        self.assertTrue(null)

    def test_image_thumbnail_transparent_upload_to(self):
        a = Article.objects.all()[0]
        upload_to = a._meta.get_field("image_thumbnail_transparent").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_thumbnail_transparent_help_text(self):
        a = Article.objects.all()[0]
        help_text = a._meta.get_field("image_thumbnail_transparent").help_text
        expected = "Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)

    def test_image_thumbnail_transparent_maximum_size(self):
        a = Article.objects.all()[0]
        size = Image.open(a.image_thumbnail_transparent).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(size <= expected)

    def test_image_thumbnail_transparent_at_least_one_dimension_is_maxed(self):
        a = Article.objects.all()[0]
        size = Image.open(a.image_thumbnail_transparent).size
        expected = settings.IMAGE_THUMBNAIL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_thumbnail_transparent_file_type(self):
        a = Article.objects.all()[0]
        image_format = Image.open(a.image_thumbnail_transparent).format
        expected = "PNG"
        self.assertEquals(image_format, expected)
    
    def test_image_thumbnail_transparent_has_alpha(self):
        a = Article.objects.all()[0]
        image_transparent = Image.open(a.image_thumbnail_transparent).getchannel("A")
        self.assertTrue(image_transparent)

    def test_image_thumbnail_transparent_name(self):
        a = Article.objects.all()[0]
        name = a.image_thumbnail_transparent.name
        expected = "uploads/test_image_thumbnail_transparent.png"
        self.assertEquals(name, expected)

    def test_image_full_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("image_full").verbose_name
        expected = "image full"
        self.assertEquals(label, expected)

    def test_image_full_blank(self):
        a = Article.objects.all()[0]
        blank = a._meta.get_field("image_full").blank
        self.assertTrue(blank)

    def test_image_full_null(self):
        a = Article.objects.all()[0]
        null = a._meta.get_field("image_full").null
        self.assertTrue(null)

    def test_image_full_upload_to(self):
        a = Article.objects.all()[0]
        upload_to = a._meta.get_field("image_full").upload_to
        expected = "uploads/"
        self.assertEquals(upload_to, expected)

    def test_image_full_help_text(self):
        a = Article.objects.all()[0]
        help_text = a._meta.get_field("image_full").help_text
        expected = "Will be auto-generated from image_raw; leave blank"
        self.assertEquals(help_text, expected)
    
    def test_image_full_maximum_size(self):
        a = Article.objects.all()[0]
        size = Image.open(a.image_full).size
        expected = settings.IMAGE_FULL_SIZE
        self.assertTrue(size <= expected)

    def test_image_full_at_least_one_dimension_is_maxed(self):
        a = Article.objects.all()[0]
        size = Image.open(a.image_full).size
        expected = settings.IMAGE_FULL_SIZE
        self.assertTrue(
            size[0] == expected[0] or
            size[1] == expected[1]
        )

    def test_image_full_file_type(self):
        a = Article.objects.all()[0]
        image_format = Image.open(a.image_full).format
        expected = "PNG"
        self.assertEquals(image_format, expected)

    def test_image_full_name(self):
        a = Article.objects.all()[0]
        name = a.image_full.name
        expected = "uploads/test_image_full.png"
        self.assertEquals(name, expected)

    def test_audio_label(self):
        a = Article.objects.all()[0]
        expected = "audio"
        label = a._meta.get_field("audio").verbose_name
        self.assertEquals(expected, label)

    def test_audio_upload_to(self):
        a = Article.objects.all()[0]
        expected = "uploads/audio"
        upload = a._meta.get_field("audio").upload_to
        self.assertEquals(expected, upload)

    def test_audio_blank(self):
        a = Article.objects.all()[0]
        blank = a._meta.get_field("audio").blank
        self.assertTrue(blank)

    def test_audio_null(self):
        a = Article.objects.all()[0]
        null = a._meta.get_field("audio").null
        self.assertTrue(null)

    def test_audio_default(self):
        a = Article.objects.all()[0]
        audio = repr(a.audio)
        expected = "<FieldFile: None>"
        self.assertEquals(audio, expected)

    def test_enabled_label(self):
        a = Article.objects.all()[0]
        label = a._meta.get_field("enabled").verbose_name
        expected = "enabled"
        self.assertEquals(label, expected)

    def test_enabled_help_text(self):
        a = Article.objects.all()[0]
        expected = "If this article should be accessible to the public or not"
        help_text = a._meta.get_field("enabled").help_text
        self.assertEquals(expected, help_text)

    def test_enabled_default(self):
        a = Article.objects.all()[0]
        enabled = a.enabled
        self.assertTrue(enabled)

    def test_str_is_title(self):
        a = Article.objects.all()[0]
        expected = "Test Article"
        self.assertEquals(str(a), expected)

    def test_get_absolute_url(self):
        a = Article.objects.all()[0]
        expected = "/articles/test-series/test-article"
        url = a.get_absolute_url()
        self.assertEquals(url, expected)

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_has_been_modified_returns_zero_if_modified_too_soon(self):    
        a = Article.objects.all()[0]
        a.title = "changed title"
        a.save()
        a.refresh_from_db()
        expected = 0
        mod = a.has_been_modified()
        self.assertEquals(mod, expected)

    @patch("articles.models.timezone.now", fake_later)
    def test_has_been_modified_shows_days(self):
        a = Article.objects.all()[0]
        a.title = "changed title"
        a.save()
        a.refresh_from_db()
        expected = 1
        mod = a.has_been_modified()
        self.assertEquals(mod, expected)

    @patch("articles.models.timezone.now", fake_later)
    def test_get_available_articles_shows_all_enabled_and_published_articles(self):
        s = Series.objects.all()[0]
        for x in range(5):
            Article.objects.create(
                title = "Article" + str(x),
                content = "article" + str(x),
                shortline = "short",
                series = s
            )
        expected = Article.objects.all()
        available = Article.get_available_articles()
        # https://stackoverflow.com/a/49129560/10225688
        # Transform argument causes the assert to not call rep() on models, which yields a false negative
        self.assertQuerysetEqual(available, expected, transform=lambda x: x)

    @patch("articles.models.timezone.now", fake_later)
    def test_get_available_articles_ignores_disabled_articles(self):
        s = Series.objects.all()[0]
        for x in range(10):
            Article.objects.create(
                title = "Article" + str(x),
                content = "article",
                shortline = "short",
                series = s,
                enabled = bool(x % 2)
            )
        expected = 6
        available = len(Article.get_available_articles())
        self.assertEquals(expected, available)

    @patch("articles.models.timezone.now", fake_slightly_later)
    def test_get_available_articles_ignores_future_publish_articles(self):
        s = Series.objects.all()[0]
        for x in range(10):
            pub_date = fake_now() if x % 2 else fake_later()
            Article.objects.create(
                title = "Article" + str(x),
                content = "article",
                shortline = "short",
                series = s,
                publish_date = pub_date
            )
        expected = 6
        available = len(Article.get_available_articles())
        self.assertEquals(available, expected)

    @patch("articles.models.timezone.now", fake_later)
    def test_visible_is_true_for_enabled_and_published_articles(self):
        a = Article.objects.all()[0]
        visible = a.visible()
        self.assertTrue(visible)

    @patch("articles.models.timezone.now", fake_later)
    def test_visible_is_false_for_disabled_articles(self):
        a = Article.objects.all()[0]
        a.enabled = False
        a.save()
        a.refresh_from_db()
        visible = a.visible()
        self.assertFalse(visible)

    @patch("articles.models.timezone.now", fake_now)
    def test_visible_is_false_for_future_publishing_articles(self):
        a = Article.objects.all()[0]
        a.publish_date = fake_later()
        a.save()
        a.refresh_from_db()
        visible = a.visible()
        self.assertFalse(visible)
