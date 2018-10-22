# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from news_site.models import Category, Article
from rest_framework.authtoken.models import Token

from rest_framework import generics
from rest_framework.views import APIView

from .serializers import CategorySerializer, ArticleSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django_ft_news_site.constants import default_categories


class SignUpAPIView(APIView):

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"msg": "sign up successfully",
                             "key": token.key,
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
        return Response({'token': token.key},
                        status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


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
        if article_id.isdigit():
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
