import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.query import QuerySet


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(help_text="I mean. It's a bio.")
    image = models.ImageField(blank=True, upload_to="uploads/")
    slug = models.SlugField(
        help_text = "A no space name to be used for URLs",
        blank = True,
        null = True,
        editable = False
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #pylint: disable=E1101
        return reverse('author-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Series(models.Model):
    name = models.CharField(max_length=40, help_text="The series this article should be filed under; will be used for URLs", unique=True)
    description = models.TextField(default="", help_text="A description of the series")
    slug = models.SlugField(
        help_text="The short version of the name to use in URLs",
        null = True,
        editable = False,
        blank = True
    )
    image = models.ImageField(upload_to="uploads/", blank=True)
    latest_article_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        #pylint: disable=E1101
        return reverse('series-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def latest_list(self) -> QuerySet:
        #pylint: disable=E1101
        articles = self.article_set.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )
        if articles:
            return articles[:5]
        else:
            return None

    def latest_article(self) -> "Article":
        #pylint: disable = E1101
        return self.article_set.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )[:1][0]

    class Meta:
        verbose_name_plural = "series"
        ordering = ["-latest_article_date"]

class Tag(models.Model):
    name = models.CharField(max_length=200, help_text="Tags used to help search for articles", unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        #pylint: disable=E1101
        return reverse('tag-detail', args=[self.name])

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        help_text="Slugs are short versions of the title used for URLs",
        blank = True,
        null = True,
        editable = False,
    )
    content = models.TextField(help_text="Unlimited length. HTML formatted.")
    shortline = models.CharField(max_length=200, help_text="A short summary to show in the sidebar and under the article title")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    series = models.ForeignKey('Series', on_delete=models.SET_DEFAULT, default=0)
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(upload_to="uploads/", blank=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        get_latest_by: "-publish_date"
        ordering = ["-publish_date", "-date_modified"]

    def __str__(self):
        return "{0}/{1}".format(self.series, self.slug)

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.series, self.slug])

    @property
    def has_been_modified(self):
        d = self.date_modified - self.publish_date
        try:
            r = d.days
        except AttributeError:
            r = 0
        return r

    def save(self, *args, **kwargs):
        #pylint: disable=E1101
        if not self.slug:
            self.slug = slugify(self.title)
        if self.series.latest_article_date is None or self.series.latest_article_date < self.publish_date:
            self.series.latest_article_date = self.publish_date
            self.series.save()
        super().save(*args, **kwargs)

    @classmethod
    def get_available_articles(cls):
        # pylint: disable=E1101
        return cls.objects.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )

    def visible(self) -> bool:
        return self.enabled and self.publish_date <= timezone.now()