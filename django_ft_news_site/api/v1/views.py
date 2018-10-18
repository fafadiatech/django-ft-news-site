# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from news_site.models import Category, Article, Source

from rest_framework import generics
from rest_framework.views import APIView

from .serializers import CategorySerializer, ArticleSerializer

from rest_framework.response import Response
from rest_framework import status

from django_ft_news_site.constants import default_categories


# Create your views here.


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleListAPIView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        """
        This method is used to fetech articles base on the user passion
        """
        user = request.user
        article_id = self.kwargs.get("article_id", "")
        if article_id:
            article = Article.objects.filter(id=article_id).first()
            if article:
                return Response(ArticleSerializer(article).data)
            else:
                return Response("Article Not Found")
        if user.is_anonymous:
            return Response(ArticleSerializer(Article.objects.filter(
                category__name__in=default_categories), many=True).data)

        else:
            return Response(
                ArticleSerializer(Article.objects.all(), many=True).data)
