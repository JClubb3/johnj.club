from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        
class Series(models.Model):
    name = models.CharField(max_length=40, help_text="The series this article should be filed under; will be used for URLs", unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, help_text="Tags used to help search for articles")

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(help_text="Slugs are short versions of the title used for URLs")
    content = models.TextField()
    shortline = models.CharField(max_length=200, help_text="A short summary to show in the sidebar and under the article title")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modifed = models.DateTimeField(auto_now=True, editable=False)
    series = models.ForeignKey('Series', on_delete=models.SET_DEFAULT, default=0)
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(upload_to="uploads/", blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.title