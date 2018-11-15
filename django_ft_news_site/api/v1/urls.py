from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (CategoryListAPIView, ArticleListAPIView, SignUpAPIView,
                    LoginAPIView, LogoutAPIView, SourceListAPIView,
                    ArticleDetailAPIView, ArticleBookMarkAPIView,
                    ArticleRecommendationsAPIView, GetBookmarkArticlesAPIView,
                    ForgotPasswordAPIView, ChangePasswordAPIView)

urlpatterns = [
    url(r'^categories/$', CategoryListAPIView.as_view(),
        name="category-list"),
    url(r'^articles/$', ArticleListAPIView.as_view(),
        name="articles-list"),
    url(r'^bookmark-articles/$', GetBookmarkArticlesAPIView.as_view(),
        name="bookmark-articles"),
    url(r'^source/$', SourceListAPIView.as_view(),
        name="source-list"),
    url(r'^articles/vote/$', ArticleDetailAPIView.as_view(),
        name="vote-article"),
    url(r'^articles/bookmark/$', ArticleBookMarkAPIView.as_view(),
        name="bookmark-article"),
    url(r'^articles/(?P<article_id>[-\d]+)/$', ArticleDetailAPIView.as_view(),
        name="articles-list"),
    url(r'^articles/(?P<article_id>[-\d]+)/recommendations/$',
        ArticleRecommendationsAPIView.as_view(),
        name="articles-list"),
    url(r'^search/$', ArticleListAPIView.as_view(),
        name="article-search"),
    url(r'^signup/$', SignUpAPIView.as_view(),
        name="signup"),
    url(r'^login/$', LoginAPIView.as_view(),
        name="login"),
    url(r'^logout/$', LogoutAPIView.as_view(),
        name="logout"),
    url(r'^forgot-password/$', ForgotPasswordAPIView.as_view(),
        name="forgot-password"),
    url(r'^change-password/$', ChangePasswordAPIView.as_view(),
        name="change-password"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
