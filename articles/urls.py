from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<slug:slug>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('articles/series', views.SeriesListView.as_view(), name='series-list'),
    path('articles/series/<slug:slug>', views.SeriesDetailView.as_view(), name='series-detail'),
    path('articles/tags', views.TagListView.as_view(), name='tag-list'),
    path('articles/tags/<slug:tag>', views.TagDetailView.as_view(), name='tag-detail'),
    path('articles', views.ArticleListView.as_view(), name='article-list'),
    path('articles/<slug:series>/<slug:slug>', views.ArticleDetailView.as_view(), name='article-detail'),
]