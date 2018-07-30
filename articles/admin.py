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
    list_display = ('slug', 'series', 'author', 'date_posted', 'date_modified', "enabled")
    fields = ('title', 'enabled','series', 'slug', 'shortline', 'author', 'tags', 'image', 'content')
    filter_horizontal = ['tags']
    list_filter = ('series', 'enabled', 'author', 'date_posted', 'date_modified', 'tags')
    #inlines = [TagInline, SeriesInline]
