from rest_framework import serializers
from news_site.models import Category, Article, UserProfile
# from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'source', 'category', 'sub_category', 'source_url',
                  'cover_image', 'blurb', 'published_on')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password')

    def validate(self, data):
        if "email" not in data.keys() or data["email"] == "":
            raise serializers.ValidationError("Email Field Is Required")
            if data["password"] == "":
                raise serializers.ValidationError("Password Field Is Required")
        return data
