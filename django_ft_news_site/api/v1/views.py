# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from news_site.models import Category, Article, Source
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView

from .serializers import (CategorySerializer, ArticleSerializer, UserSerializer,
                          SourceSerializer)

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django_ft_news_site.constants import default_categories
from django.db.models import Q
from rest_framework.exceptions import APIException


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.set_password(request.data["password"])
            user.save()
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"Msg": "sign up successfully",
                             "Token": token.key,
                             "status": status.HTTP_201_CREATED})
        else:
            return Response({'error': user_serializer.errors},
                            status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({
                'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id,
                         'username': user.username}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CategoryListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, *args, **kwargs):
        """
        List all news category
        """
        categories = CategorySerializer(Category.objects.all(), many=True)
        return Response({"categories": categories.data})

    def post(self, request, format=None):
        """
        Save new category to database
        """
        serializer = CategorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SourceListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, *args, **kwargs):
        """
        List all news category
        """
        source = SourceSerializer(Source.objects.all(), many=True)
        return Response({"source": source.data})


class NoarticleFound(APIException):
    """
    api exception for no user found
    """
    status_code = 404
    default_detail = ("Article does not exist")
    default_code = "no_article_found"


class ArticleListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, *args, **kwargs):
        """
        This method is used to fetech articles base on the user passion
        """
        user = request.user
        article_id = self.kwargs.get("article_id", "")
        article_desc = self.request.GET.get("q", "")
        if article_id:
            if article_id.isdigit():
                article = Article.objects.filter(id=article_id).first()
                if article:
                    return Response(
                        {"article": ArticleSerializer(article).data})
                else:
                    raise NoarticleFound
            else:
                raise NoarticleFound

        elif article_desc:
            articles = Article.objects.filter(Q(
                title__icontains=article_desc) |
                Q(full_text__icontains=article_desc))
            return Response({"articles": ArticleSerializer(
                articles, many=True).data})
        if user.is_anonymous:
            return Response({"articles": ArticleSerializer(
                Article.objects.filter(category__name__in=default_categories),
                many=True).data})

        elif user.passion.all().count() > 0:
            passion = user.passion.all().values_list("name", flat=True)
            return Response({"articles": ArticleSerializer(
                Article.objects.filter(category__name__in=passion),
                many=True).data})
        else:
            return Response({"articles": ArticleSerializer(
                Article.objects.all(), many=True).data})

    def post(self, request, format=None, *args, **kwargs):
        categories = request.data.getlist("categories")
        articles = Article.objects.filter(category__name__in=categories)

        return Response({"articles": ArticleSerializer(articles,
                                                       many=True).data})
