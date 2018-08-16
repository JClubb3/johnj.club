import pytz

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from PIL import Image
from datetime import datetime, timedelta
from mock import patch

from articles.models import Author, Series, Tag, Article

IMAGE_PATH = "articles/tests/test_image.jpg"

TZ = pytz.timezone("America/New_York")

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

def fake_later():
    return fake_now() + timedelta(days=1)

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


    