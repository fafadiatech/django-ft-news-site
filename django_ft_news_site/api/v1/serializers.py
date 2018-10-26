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
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        if "email" not in data.keys() or data["email"] == "":
            raise serializers.ValidationError(
                {"email": "Email Field Is Required"})
        if "password" not in data.keys() or data["password"] == "":
            raise serializers.ValidationError(
                {"password": "Password Field Is Required"})

        if "first_name" not in data.key() or data["first_name"] == "":
            raise serializers.ValidationError(
                {"first_name": "First name Is Required"})

        if "last_name" not in data.key() or data["last_name"] == "":
            raise serializers.ValidationError(
                {"last_name": "Last name Is Required"})
        return data


{
    "header": {
        "status": "0"
    },
    "errors": {
        "errorList": [
            {
                "field": "password",
                "field_error": "This field is required."
            }
        ]
    }
}

{
    "header": {
        "status": "0"
    },
    "errors": {
        "error": {
            "email": [
                "Email Field Is Required"
            ]
        }
    }
}

{
    "header": {
        "status": "0"
    },
    "errors": {
        "errorList": [
            {
                "field": "password",
                "field_error": "This field is required."
            },
            {
                "field": "email",
                "field_error": "This field is required."
            }
        ]
    }
}


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if user:
            return user
        raise serializers.ValidationError(
            "Unable to log in with provided credentials.")
