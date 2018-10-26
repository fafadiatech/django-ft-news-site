from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (CategoryListAPIView, ArticleListAPIView, SignUpAPIView,
                    LoginAPIView, LogoutAPIView, SourceListAPIView,
                    ArticleDetailAPIView)

urlpatterns = [
    url(r'^categories/$', CategoryListAPIView.as_view(),
        name="category-list"),
    url(r'^articles/$', ArticleListAPIView.as_view(),
        name="articles-list"),
    url(r'^source/$', SourceListAPIView.as_view(),
        name="source-list"),
    url(r'^articles/(?P<article_id>[-\w\d]+)/$', ArticleDetailAPIView.as_view(),
        name="articles-list"),
    url(r'^search/$', ArticleListAPIView.as_view(),
        name="article-search"),
    url(r'^signup/$', SignUpAPIView.as_view(),
        name="signup"),
    url(r'^login/$', LoginAPIView.as_view(),
        name="login"),
    url(r'^logout/$', LogoutAPIView.as_view(),
        name="logout"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
