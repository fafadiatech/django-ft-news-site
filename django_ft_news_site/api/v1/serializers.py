from rest_framework import serializers
from news_site.models import Category, Article


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'source', 'category', 'sub_category', 'source_url',
                  'cover_image', 'blurb', 'published_on')
