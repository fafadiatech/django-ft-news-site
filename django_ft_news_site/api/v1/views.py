# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from news_site.models import (Category, Article, Source, UserProfile,
                              BookmarkArticle, ArtilcleLike)
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView

from .serializers import (CategorySerializer, ArticleSerializer, UserSerializer,
                          SourceSerializer, LoginUserSerializer)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django_ft_news_site.constants import default_categories
from django.db.models import Q
from rest_framework.exceptions import APIException
from collections import OrderedDict
from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework.generics import ListAPIView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import uuid


def create_response(response_data):
    """
    method used to create response data in given format
    """
    response = OrderedDict()
    response["header"] = {"status": "1"}
    response["body"] = response_data
    return response


def create_error_response(response_data):
    """
    method used to create response data in given format
    """
    return OrderedDict({
        "header": {
            "status": "0"
        },
        "errors": response_data
    }
    )


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response(create_response(
                {"Msg": "sign up successfully",

                 }))
        else:
            return Response(
                create_serializer_error_response(user_serializer.errors),
                status=403)


class LoginFieldsRequired(APIException):
    """
    api exception for no user found
    """
    status_code = 401
    default_detail = ("username and password are required")
    default_code = "username_and_password"


def create_serializer_error_response(errors):
    """
    methos is used to create error response for serializer errors
    """
    error_list = []
    for k, v in errors.items():
        if isinstance(v, dict):
            _, v = v.popitem()
        d = {}
        d["field"] = k
        d["field_error"] = v[0]
        error_list.append(d)
    return OrderedDict({"header": {"status": "0"}, "errors": {
        "errorList": error_list}})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        if not serializer.is_valid():
            res_data = create_serializer_error_response(serializer.errors)
            return Response(res_data, status=403)

        user = UserProfile.objects.filter(email=request.data["email"]).first()
        token, _ = Token.objects.get_or_create(user=user)
        response_data = create_response(
            {'token': token.key, 'first_name': user.first_name,
             'last_name': user.last_name, 'user_id': user.id})
        return Response(response_data)


class LogoutAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(create_response({"Msg": "User has been logged out"}))


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
        serializer = CategorySerializer(data=data, many=True)
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


# class PostpageNumberPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

class PostpageNumberPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = '-created_at'


class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    pagination_class = PostpageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        This method is used to fetech articles base on the user passion
        """
        user = self.request.user
        article_desc = self.request.GET.get("q", "")
        categories = self.request.GET.get("categories", "")
        is_bookmark = "bookmark-articles" in self.request.path
        articles = Article.objects.all()
        if categories:
            categories_list = categories.split(",")
            articles = Article.objects.filter(
                category__name__in=categories_list)

        if article_desc:
            articles = articles.filter(Q(
                title__icontains=article_desc) |
                Q(full_text__icontains=article_desc))

        if user.is_anonymous:
            articles = articles.filter(category__name__in=default_categories)

        elif not user.is_anonymous and is_bookmark:
            article_id = BookmarkArticle.objects.filter(user=user).values_list(
                "article__id", flat=True)
            articles = articles.filter(id__in=article_id)

        elif user.passion.all().count() > 0:
            passion = user.passion.all().values_list("name", flat=True)
            articles = articles.filter(category__name__in=passion)

        return articles

    def list(self, request, *args, **kwargs):
        """
        override list method to add end date and create custom response
        """
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for article in serializer.data:
                if not user.is_anonymous:
                    book_mark_inst = BookmarkArticle.objects.filter(
                        article__id=article.get('id'), user=user)
                    article_inst = ArtilcleLike.objects.filter(
                        article__id=article.get('id'), user=user)
                    if book_mark_inst:
                        article["isBookMark"] = True
                    else:
                        article["isBookMark"] = False
                    if article_inst:
                        article["isLike"] = article_inst.first().is_like
                    else:
                        article["isLike"] = 2

            paginated_response = self.get_paginated_response(serializer.data)

            response_data = create_response(paginated_response.data)
            return Response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = create_response({"results": serializer.data})
        return Response(response_data)


class ArticleDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, *args, **kwargs):
        article_id = self.kwargs.get("article_id", "")

        user = self.request.user
        if article_id:
            if article_id.isdigit():
                article = Article.objects.filter(id=article_id).first()
                if article:
                    response_data = ArticleSerializer(article).data
                    if not user.is_anonymous:
                        book_mark_article = BookmarkArticle.objects.filter(
                            user=user, article=article).first()
                        like_article = ArtilcleLike.objects.filter(
                            user=user, article=article).first()

                        if book_mark_article:
                            response_data["isBookMark"] = True
                        else:
                            response_data["isBookMark"] = False

                        if like_article:
                            response_data["isLike"] = like_article.is_like
                        else:
                            response_data["isLike"] = 2

                    return Response(create_response({
                        "article": response_data}))
                else:
                    raise NoarticleFound()
            else:
                raise NoarticleFound

        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get("article_id", "")
        is_like = self.request.POST.get("isLike", "")
        user = self.request.user
        article = Article.objects.filter(id=article_id).first()
        if user and not user.is_anonymous:
            if article:
                if is_like and int(is_like) <= 2:
                    article_like, created = ArtilcleLike.objects.get_or_create(
                        user=user, article=article)
                    article_like.is_like = is_like
                    article_like.save()
                    return Response(create_response({
                        "Msg": "Article like status changed"
                    }))
                else:
                    return Response(create_error_response({
                        "Msg": "Invalid Input"
                    }))
        else:
            return Response(create_error_response({
                "Msg": "Unauthorized User"
            }))


class ArticleBookMarkAPIView(APIView):

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get("article_id", "")
        user = self.request.user
        if article_id:
            article = Article.objects.filter(id=article_id).first()
            if article:
                bookmark_article, created = \
                    BookmarkArticle.objects.get_or_create(user=user,
                                                          article=article)
                if not created:
                    bookmark_article.delete()
                    return Response(create_response({
                        "Msg": "Article removed from bookmark list"
                    }))
                else:
                    return Response(create_response({
                        "Msg": "Article bookmarked successfully"
                    }))
            else:
                raise NoarticleFound
        else:
            return Response(create_error_response({
                "Msg": "Missing Key"
            }))


class ArticleRecommendationsAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        article_id = self.kwargs.get("article_id", "")
        if article_id:
            article = Article.objects.filter(id=article_id).first()
            if article:
                articles = Article.objects.all().exclude(id=article_id)
                return Response(create_response({
                    "results": ArticleSerializer(articles, many=True).data
                }))

            else:
                raise NoarticleFound
        else:
            return Response(create_error_response({
                "Msg": "Missing Key"
            }))


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""

    # Convert UUID format to a Python string.
    random = str(uuid.uuid4())

    # Make all characters uppercase.
    random = random.upper()

    # Remove the UUID '-'.
    random = random.replace("-", "")

    # Return the random string.
    return random[0:string_length]


def send_mail_to_user(email, password, first_name="", last_name=""):
    username = first_name + " " + last_name
    email_subject = 'NewsPost: Forgot Password Request'
    email_body = """<html>
                <head>
                </head>
                <body>
                <p>
                Hello """ + username + """,<br><br><b>
                """ + password + """</b> is your new password
                <br>
                <br>
                Thanks,<br>
                The NewsPost Team<br>
                </p>
                </body>
                </html>"""

    msg = EmailMultiAlternatives(
        email_subject, '', settings.EMAIL_HOST_USER, [email])
    ebody = email_body
    msg.attach_alternative(ebody, "text/html")
    msg.send(fail_silently=False)


class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = self.request.POST.get("email", "")
        if email:
            user = UserProfile.objects.filter(email=email)
            if user:
                user = user.first()
                password = my_random_string()
                send_mail_to_user(
                    email, password, user.first_name, user.last_name)
                user.set_password(password)
                user.save()
                return Response(create_response({
                    "Msg": "New password sent to your email"
                }))
            else:
                return Response(create_error_response({
                    "Msg": "Email Does Not Exist"
                }))
        else:
            return Response(create_error_response({
                "Msg": "Missing Key"
            }))


class ChangePasswordAPIView(APIView):

    def post(self, request, *args, **kwargs):
        password = self.request.POST.get("password", "")
        old_password = self.request.POST.get("old_password", "")
        confirm_password = self.request.POST.get("confirm_password", "")
        user = self.request.user
        if old_password:
            if not user.check_password(old_password):
                msg = "Old Password Does Not Match With User"
                return Response(create_error_response({
                    "Msg": msg
                }))
            if confirm_password != password:
                msg = "Password and Confirm Password does not match"
                return Response(create_error_response({
                    "Msg": msg
                }))
            if old_password == password:
                msg = "New password should not same as Old password"
                return Response(create_error_response({
                    "Msg": msg
                }))
            if user and password:
                user.set_password(password)
                user.save()
                return Response(create_response({
                    "Msg": "Password chnaged successfully"
                }))
            else:
                return Response(create_error_response({
                    "Msg": "Password field is required"
                }))
        else:
            return Response(create_error_response({
                "Msg": "Old Password field is required"
            }))
