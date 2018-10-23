from rest_framework import serializers
from news_site.models import Category, Article, UserProfile, Source
from django.contrib.auth import authenticate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('name', )


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'source', 'category',
                  'source_url', 'cover_image', 'blurb', 'published_on')

    source = serializers.ReadOnlyField(source='source.name')
    category = serializers.ReadOnlyField(source='category.name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email',
                  'password')

    def validate(self, data):
        if "email" not in data.keys() or data["email"] == "":
            raise serializers.ValidationError("Email Field Is Required")
            if data["password"] == "":
                raise serializers.ValidationError("Password Field Is Required")
        return data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if user:
            return user
        raise serializers.ValidationError(
            "Unable to log in with provided credentials.")
