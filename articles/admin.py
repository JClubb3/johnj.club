from django.contrib import admin

from .models import Author, Series, Tag, Article

# Register your models here.
admin.site.register(Author)
admin.site.register(Series)
admin.site.register(Tag)
#admin.site.register(Article)

class TagInline(admin.TabularInline):
    model = Tag

class SeriesInline(admin.TabularInline):
    model = Series

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('slug', 'series', 'author', 'publish_date', 'date_modified', "enabled")
    fields = ('title', 'enabled','series', 'shortline', 'author', 
        'publish_date', 'tags', 'image_raw', 'image_full', 'image_thumbnail', 
        'image_thumbnail_transparent', 'audio', 'content',)
    filter_horizontal = ['tags']
    list_filter = ('series', 'enabled', 'author', 'publish_date', 'date_modified', 'tags')
    #inlines = [TagInline, SeriesInline]
