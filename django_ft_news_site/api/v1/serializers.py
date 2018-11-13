from rest_framework import serializers
from news_site.models import Category, Article, UserProfile, Source
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


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
    isLike = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'source', 'category', 'source_url',
                  'cover_image', 'blurb', 'published_on', 'is_book_mark',
                  'isLike')

    source = serializers.ReadOnlyField(source='source.name')
    category = serializers.ReadOnlyField(source='category.name')


class UserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200, required=True, validators=[
        UniqueValidator(queryset=UserProfile.objects.all(),
                        message="User with this email already exist")],)
    password = serializers.CharField(max_length=200, required=True)
    first_name = serializers.CharField(max_length=200, required=True)
    last_name = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.username = validated_data["email"]
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if user:
            return user
        raise exceptions.AuthenticationFailed('User inactive or deleted')
