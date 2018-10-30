from rest_framework import serializers
from news_site.models import Category, Article, UserProfile, Source
from django.contrib.auth import authenticate
from rest_framework import exceptions


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('name', )


class ArticleSerializer(serializers.ModelSerializer):
    is_book_mark = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'source', 'category', 'source_url',
                  'cover_image', 'blurb', 'published_on', 'is_book_mark')

    source = serializers.ReadOnlyField(source='source.name')
    category = serializers.ReadOnlyField(source='category.name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        if "email" not in data.keys() or data["email"] == "":
            raise serializers.ValidationError(
                {"email": "Email Field Is Required"})
        if "password" not in data.keys() or data["password"] == "":
            raise serializers.ValidationError(
                {"password": "Password Field Is Required"})

        if "first_name" not in data.keys() or data["first_name"] == "":
            raise serializers.ValidationError(
                {"first_name": "First name Is Required"})

        if "last_name" not in data.keys() or data["last_name"] == "":
            raise serializers.ValidationError(
                {"last_name": "Last name Is Required"})
        if UserProfile.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"Already Exists": "User with this email already exist"})
        return data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if user:
            return user
        raise exceptions.AuthenticationFailed('User inactive or deleted')
