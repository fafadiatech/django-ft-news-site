from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import CategoryListAPIView, ArticleListAPIView

urlpatterns = [
    url(r'^categories/$', CategoryListAPIView.as_view(),
        name="category-list"),
    url(r'^articles/$', ArticleListAPIView.as_view(),
        name="articles-list"),
    url(r'^articles/(?P<article_id>[-\w\d]+)/$', ArticleListAPIView.as_view(),
        name="articles-list"),

]
urlpatterns = format_suffix_patterns(urlpatterns)
