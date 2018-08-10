import datetime
import sys

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.query import QuerySet
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from PIL import Image
from typing import Union
from io import BytesIO


def _create_image(
    instance: models.Model, 
    size: tuple, 
    suffix: str,
    set_alpha: bool = False
    ) -> InMemoryUploadedFile:
    """
    Creates a new image based on the `instance.image_raw`, ready for upload.

    This code was modified from https://djangosnippets.org/snippets/10597/

    Takes an incoming instance of a model, accesses that instance's `image_raw`
    field, and creates a new image. The new image will have its deminsions set
    by the `size` argument, and have the `suffix` appended to its name. If 
    `set_alpha` is true, will also have a 50% alpha layer added. The new image
    will be a PNG. The new image will be ready to be added as a field to a
    model.
    
    Args:
        instance (models.Model): The instance of a model. This instance must
            have an image set to the `image_raw` field.
        size (tuple): The dimensions the new image will have.
        suffix (str): A string to append to the end of the image's name.
        set_alpha (bool, optional): Defaults to False. Weather or not a 50%
            alpha layer should be added to the image.
    
    Returns:
        InMemoryUploadedFile: The new image, saved in memory and ready to be
            set to a field on the instance and uploaded.
    """

    image = Image.open(instance.image_raw)
    output = BytesIO() # Don't want to write to disk, so we use memory instead.
    base_name = instance.image_raw.name.split(".")[0]

    resized = image.copy()
    resized.thumbnail(size, Image.ANTIALIAS) # Thumbnail modifies in-place.
    resized_name = "{0}_{1}.png".format(base_name, suffix)
    
    if set_alpha:
        resized.putalpha(127) # Putalpha also modifies in-place.

    resized.save(output, format="PNG", quality=100)
    output.seek(0)
    
    prepped_image = InMemoryUploadedFile(
        output,
        'ImageField',
        resized_name,
        'image/png',
        sys.getsizeof(output),
        None
    )
    return prepped_image

def create_image_thumbnail(instance: models.Model):
    """
    Adds a modified version of `instance.image_raw` to `instance.image_thumbnail`.

    The settings file must have an attribute `IMAGE_THUMBNAIL_SIZE` which must
    contain a tuple holding the size dimensions of the thumbnail image.
    
    Args:
        instance (models.Model): The instance to which the thumbnail image
            should be added. The instance must have an image in the `image_raw`
            field and have an `image_thumbnail` field.
    """

    img = _create_image(instance, settings.IMAGE_THUMBNAIL_SIZE, "thumbnail")
    instance.image_thumbnail = img

def create_image_thumbnail_transparent(instance: models.Model):
    """
    Adds a modified version of `instance.image_raw` to `instance.image_thumbnail_transparent`.

    The settings file must have an attribute `IMAGE_THUMBNAIL_SIZE` which must
    contain a tuple holding the size dimensions of the thumbnail image.
    
    Args:
        instance (models.Model): The instance to which the transparent 
            thumbnail image should be added. The instance must have an image 
            in the `image_raw` field and have an `image_thumbnail_transparent` 
            field.
    """

    img = _create_image(
        instance, settings.IMAGE_THUMBNAIL_SIZE, 
        "thumbnail_transparent", 
        set_alpha=True
    )
    instance.image_thumbnail_transparent = img

def create_image_full(instance: models.Model):
    """
    Adds a modified version of `instance.image_raw` to `instance.image_full`.

    The settings file must have an attribute `IMAGE_FULL_SIZE` which must
    contain a tuple holding the size dimensions of the image.
    
    Args:
        instance (models.Model): The instance to which the full-sized image 
            should be added. The instance must have an image in the `image_raw` 
            field and have an `image_full` field.
    """

    img = _create_image(instance, settings.IMAGE_FULL_SIZE, "full")
    instance.image_full = img

# Create your models here.
class Author(models.Model):
    """
    Used to attribute Articles to particular people.

    This could instead be or derived from Django's User model, but I simply
    didn't think of that until I had already built a lot. Can be refactored
    in the future to use User instead.
    
    Attributes:
        name (CharField): The name of the Author. Max length 200 and must by
            unique.
        bio (TextField): A brief description of who the Author is, what they
            like, etc.
        image_raw (ImageField): A base image to be used to represent this
            author. The image in this field will be manipulated to
            automatically generate the images for the other image fields.
        image_thumbnail (ImageField): A much smaller version of `image_raw`.
            Dimensions for this image are in settings.IMAGE_THUMBNAIL_SIZE.
            Should generally be left blank. Will be automatically created
            when the model is saved if `image_raw` exists.
        image_thumbnail_transparent (ImageField): A smaller version of
            `image_raw`, but with an alpha layer added. The dimensions for
            this image are also in settings.IMAGE_THUMBNAIL_SIZE. Should
            generally be left blank. Will be automatically created
            when the model is saved if `image_raw` exists.
        image_full (ImageField): A larger image based on `image_raw`. The
            dimensions of this image are in settings.IMAGE_FULL_SIZE. This may
            not necessarily be larger than `image_full`, but should be larger
            than `image_thumbnail`. Should generally be left blank. Will be 
            automatically created when the model is saved if `image_raw` 
            exists.
        slug (SlugField): A slug based on the instance's name. Will be
            automatically generated on save. Used for URLs. Not editable.

    """

    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(help_text="I mean. It's a bio.")
    image_raw = models.ImageField(
        blank=True, 
        upload_to="uploads/",
        help_text = "A base image that will be manipulated to generate other image fields."
    )
    image_thumbnail = models.ImageField(
        blank = True, 
        null = True,
        upload_to = "uploads/", 
        help_text = "A smaller version of the base image. Will be auto-generated from image_raw; leave blank"
    )
    image_thumbnail_transparent = models.ImageField(
        blank = True,
        null = True,
        upload_to = "uploads/",
        help_text = "A smaller version of the base image, with an alpha layer. Will be auto-generated from image_raw; leave blank"
    )
    image_full = models.ImageField(
        blank = True,
        null = True,
        upload_to = "uploads/",
        help_text = "A good-sized version of the base image. Will be auto-generated from image_raw; leave blank"
    )
    slug = models.SlugField(
        help_text = "A no space name to be used for URLs",
        blank = True,
        null = True,
        editable = False
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        """
        Returns the URL of the Author as a str.
        
        Returns:
            str: The Author's URL.
        """

        #pylint: disable=E1101
        return reverse('author-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Sets the Author's slug and images.

        This method does two basic tasks before saving the model. First, it
        will set `self.slug` to a slugified version of `self.name`. Second,
        it manipulates `self.image_raw` to generate the images to be used
        for the other image fields.

        Args:
            *args: Not used here; called because Django expects it.
            **kwargs: Not used here; called because Django expects it.
        """

        if not self.slug:
            self.slug = slugify(self.name)
        if self.image_raw:
            if not self.image_thumbnail:
                create_image_thumbnail(self)
            if not self.image_thumbnail_transparent:
                create_image_thumbnail_transparent(self)
            if not self.image_full:
                create_image_full(self)
        super().save(*args, **kwargs)

class Series(models.Model):
    """
    These are used to contain a set of Articles of similar themes.

    Series are intended to be used similar to a folder. URLs for Articles
    include the Series. Series should be about a particular theme, with every
    Article in that Series fitting into that theme.
    
    Attributes:
        name (CharField): The name of the series. The slug will be generated
            from this name. Max length 40 and must be unique.
        description (TextField): A description of the series. Should be short
            and succinct, but max length is not enforced.
        slug (SlugField): A slug based on the `name` attribute, to be used for
            URLs. This will be automatically created when the instance is first 
            saved, and is uneditable.
        image_raw (ImageField): A base image to be used to represent this
            author. The image in this field will be manipulated to
            automatically generate the images for the other image fields.
        image_thumbnail (ImageField): A much smaller version of `image_raw`.
            Dimensions for this image are in settings.IMAGE_THUMBNAIL_SIZE.
            Should generally be left blank. Will be automatically created
            when the model is saved if `image_raw` exists.
        image_thumbnail_transparent (ImageField): A smaller version of
            `image_raw`, but with an alpha layer added. The dimensions for
            this image are also in settings.IMAGE_THUMBNAIL_SIZE. Should
            generally be left blank. Will be automatically created
            when the model is saved if `image_raw` exists.
        image_full (ImageField): A larger image based on `image_raw`. The
            dimensions of this image are in settings.IMAGE_FULL_SIZE. This may
            not necessarily be larger than `image_full`, but should be larger
            than `image_thumbnail`. Should generally be left blank. Will be 
            automatically created when the model is saved if `image_raw` 
            exists.
        latest_article_date (DateTimeField): The datetime the newest Article
            of this Series was published. This should not be set manually; will
            be set automatically when an Article is saved. This is used to
            order Series.
        
    """

    name = models.CharField(
        max_length = 40, 
        help_text = "The series this article should be filed under; will be used for URLs", 
        unique = True
    )
    description = models.TextField(
        default = "", 
        help_text = "A short description of the series"
    )
    slug = models.SlugField(
        help_text="The short version of the name to use in URLs",
        null = True,
        editable = False,
        blank = True
    )
    image_raw = models.ImageField(
        blank = True, 
        null = True,
        upload_to = "uploads/",
        help_text = "A base image that will be manipulated to generate other image fields."
    )
    image_thumbnail = models.ImageField(
        blank = True, 
        null = True,
        upload_to = "uploads/", 
        help_text = "A smaller version of the base image. Will be auto-generated from image_raw; leave blank"
    )
    image_thumbnail_transparent = models.ImageField(
        blank = True,
        null = True,
        upload_to = "uploads/",
        help_text = "A smaller version of the base image, with an alpha layer. Will be auto-generated from image_raw; leave blank"
    )
    image_full = models.ImageField(
        blank = True,
        null = True,
        upload_to = "uploads/",
        help_text = "A good-sized version of the base image. Will be auto-generated from image_raw; leave blank"
    )
    latest_article_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text = "The date and time the newest Article of this Series was published. Will be set automatically when an Article is created."
    )

    def __str__(self):
        return self.slug

    def get_absolute_url(self) -> str:
        """
        Returns the URL of the Series as a string.
        
        Returns:
            str: The URL of the Series.
        """

        #pylint: disable=E1101
        return reverse('series-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Sets the Series' slug and images.

        This method does two basic tasks before saving the model. First, it
        will set `self.slug` to a slugified version of `self.name`. Second,
        it manipulates `self.image_raw` to generate the images to be used
        for the other image fields.

        Args:
            *args: Not used here; called because Django expects it.
            **kwargs: Not used here; called because Django expects it.
        """

        if not self.slug:
            self.slug = slugify(self.name)
        if self.image_raw:
            if not self.image_thumbnail:
                create_image_thumbnail(self)
            if not self.image_thumbnail_transparent:
                create_image_thumbnail_transparent(self)
            if not self.image_full:
                create_image_full(self)
        super().save(*args, **kwargs)

    def latest_list(self) -> Union[QuerySet, None]:
        """
        Returns the latest five Articles of this Series.

        If this Series has no Articles, it will instead return None.
        
        Returns:
            Union[QuerySet, None]: Either the QuerySet of the latest
                Articles, or None if no Articles could be found.
        """

        #pylint: disable=E1101
        articles = self.article_set.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )
        return articles[:5] if articles else None

    def latest_article(self) -> Union["Article", None]:
        """
        Returns the single latest Article if it exists, None otherwise.
        
        Returns:
            Union[Article, None]: Either the laest Article or None if
                no Articles could be found.
        """

        articles = self.latest_list()[0]
        return articles[0] if articles else None

    class Meta:
        """
        Meta options for Series.

        Attributes:
            verbose_name_plural (str): Sets the pluarl name to Series instead
                of the default Seriess
            ordering (list): Sets default ordering for Series to
                `latest_article_date`, descending.
        """

        verbose_name_plural = "series"
        ordering = ["-latest_article_date"]

class Tag(models.Model):
    """
    Short words to tag concepts to Articles. Currently not used for anything.
    
    Attributes:
        name (CharField): The name of the tag. Max length of 200 and must be 
            unique.
    """

    name = models.CharField(
        max_length=200, 
        help_text="Tags used to help search for articles", 
        unique=True
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL of the Tag.
        
        Returns:
            str: The Tag's URL.
        """

        #pylint: disable=E1101
        return reverse('tag-detail', args=[self.name])

class Article(models.Model):
    """
    An Article, with content and so on.
    
    Attributes:
        title (CharField): The Article's title. Max length 200 and must be
            unique, because it is used to generate slugs.
        slug (SlugField): A URL-compliant version of the title, used for
            URLs. Will be automatically generated when the Article is first
            saved. Not editable.
        content (TextField): The actual content of the Article. The intention
            is this will allow HTML editting, since only trusting actors
            will be using this. If untrusted actors are a concern, it would
            be safed to install a Markdown formatter and use Markdown instead
            of HTML for markup.
        shortline (CharField): A short description of the Article. Used as a
            teaser. Max length 200.
        author (ForeignKey): The person who wrote this Article. Author is not
            tied to Django's User model and so should be set manually.
        publish_date (DateTimeField): The date and time at which this Article
            should become visible. May be set to a time in the future to time-
            delay an already complete Article. Articles for which `publish_date`
            is still in the future relative to real time (irrespective of time
            zones) will not be acessible to visitors.
        date_modified (DateTimeField): The last time this Article had anything
            changed. Automatic and uneditable.
        date_created (DateTimeField): The date and time this Article was
            actually created (note the disctinction between this and 
            `publish_date`). Automatic and uneditable.
        series (ForeignKey): The Series to which this Article belongs. All
            Articles belong to a Series, and the Series will be part of the
            Article's absolute url.
        tags (ManyToManyField): Any Tags that should be associated with this
            Article. Currently not used for anything.
        image_raw (ImageField): A base image to represent this Article. Will
            appear in lists of Articles, as well as prominently at the top
            of the Article's page. 
        image_thumbnail (ImageField): A much smaller version of `image_raw`.
            Dimensions for this image are in settings.IMAGE_THUMBNAIL_SIZE.
            Should generally be left blank. Will be automatically created
            when the model is saved if `image_raw` exists.
        image_thumbnail_transparent (ImageField): A smaller version of
            `image_raw`, but with an alpha layer added. The dimensions for
            this image are also in settings.IMAGE_THUMBNAIL_SIZE. Should
            generally be left blank. Will be automatically created
            when the model is saved if `image_raw` exists.
        image_full (ImageField): A larger image based on `image_raw`. The
            dimensions of this image are in settings.IMAGE_FULL_SIZE. This may
            not necessarily be larger than `image_full`, but should be larger
            than `image_thumbnail`. Should generally be left blank. Will be 
            automatically created when the model is saved if `image_raw` 
            exists.
        audio (FileField): Any audio that should be associated with this
            Article. A player will appear in the Article's detail page.
            This field is intended to be used with DnD sessions, and so is
            highly idiomatic to my personal use-case.
        enabled (BooleanField): Whether or not this Article should be
            accessible to guests. Articles for which `enabled` is False
            will not be visitable for guests.
    """

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
    image_raw = models.ImageField(
        blank = True, 
        null = True,
        upload_to = "uploads/images"
    )
    image_thumbnail = models.ImageField(
        blank = True, 
        null = True,
        upload_to = "uploads/images", 
        help_text = "Will be auto-generated from image_raw; leave blank"
    )
    image_thumbnail_transparent = models.ImageField(
        blank = True,
        null = True,
        upload_to = "uploads/images",
        help_text = "Will be auto-generated from image_raw; leave blank"
    )
    image_full = models.ImageField(
        blank = True,
        null = True,
        upload_to = "uploads/images",
        help_text = "Will be auto-generated from image_raw; leave blank"
    )
    audio = models.FileField(
        upload_to = "uploads/audio",
        blank = True,
        null = True
    )
    enabled = models.BooleanField(default=True)

    class Meta:
        """
        Meta options for Article.

        Attributes:
            get_latest_by (str): The field that will be used to determine
                which Article is the neweset. Set to `publish_date`, 
                descending.
            odering (list): Default ordering of Articles. Sorts by 
                `publish_date` (descending) first, and then by `date_modified`
                within that `publish_date`, also descending.
        """

        get_latest_by: "-publish_date"
        ordering = ["-publish_date", "-date_modified"]

    def __str__(self):
        return "{0}/{1}".format(self.series, self.slug)

    def get_absolute_url(self) -> str:
        """
        Returns the URL of the Article as a string.
        
        Returns:
            str: The absolute URL of the Article.
        """

        return reverse('article-detail', args=[self.series, self.slug])

    def has_been_modified(self) -> int:
        """
        Determines if this Article has been modified after publishing.

        This allows for a short grace window before recognizing the Article
        as having been editted. That is set to 1 day currently.
        
        Returns:
            int: The amount of days that have passed since `publish_date`.
        """

        d = self.date_modified - self.publish_date
        try:
            r = d.days
        except AttributeError:
            r = 0
        return r

    def save(self, *args, **kwargs):
        """
        Sets the Article's slug, images, and related `Series.latest_article_date`.

        The slug will be a slugified version of the Article's `title`. Images
        are all derived from `image_raw` and are modified versions of that.
        The related Series of this Article also has its `latest_article_date`
        set to this Article's `publish_date`.

        Args:
            *args: Not used here; included because Django expects it.
            **kwargs: Not used here; included because Django expects it.
        """

        #pylint: disable=E1101
        if not self.slug:
            self.slug = slugify(self.title)
        if self.series.latest_article_date is None or self.series.latest_article_date < self.publish_date:
            self.series.latest_article_date = self.publish_date
            self.series.save()
        if self.image_raw:
            if not self.image_thumbnail:
                create_image_thumbnail(self)
            if not self.image_thumbnail_transparent:
                create_image_thumbnail_transparent(self)
            if not self.image_full:
                create_image_full(self)
        super().save(*args, **kwargs)

    @classmethod
    def get_available_articles(cls) -> QuerySet:
        """
        Returns Articles that should be acceissble to visitors.

        For the most part, Articles should be accessed from this QuerySet,
        which checks if the Article has a valid `publish_date` and if the
        Article has `enabled` equal to True.

        Returns:
            QuerySet: All those Articles that should be accessible to visitors.
        """
        # pylint: disable=E1101
        return cls.objects.filter(
            enabled = True,
            publish_date__lte = timezone.now()
        )

    def visible(self) -> bool:
        """
        Returns whether or not this Article should be accesible to guests.
        
        Returns:
            bool: If visitors should be able to access this Article.
        """

        return self.enabled and self.publish_date <= timezone.now()