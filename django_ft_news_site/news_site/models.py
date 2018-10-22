# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser


class NewsSiteBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name="Last Modified At")

    class Meta:
        abstract = True


class Category(NewsSiteBaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name


class SubCategory(NewsSiteBaseModel):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __unicode__(self):
        return "%s > %s" % (self.category, self.name)


class UserProfile(AbstractUser):
    passion = models.ManyToManyField(Category, blank=True)

    def __unicode__(self):
        return "%s > %s" % (self.email, self.passion.all())


class Industry(NewsSiteBaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Industries"

    def __unicode__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class HashTag(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Article(NewsSiteBaseModel):
    title = models.CharField(max_length=600)
    source = models.ForeignKey(Source)
    category = models.ForeignKey(Category)
    sub_category = models.ForeignKey(
        SubCategory, blank=True, null=True, default=None)
    hash_tags = models.ManyToManyField(
        HashTag, blank=True, null=True, default=None)
    industry = models.ForeignKey(Industry, blank=True, null=True, default=None)
    source_url = models.URLField()
    cover_image = models.URLField(max_length=600)
    blurb = models.TextField(blank=True, null=True)
    full_text = models.TextField()
    published_on = models.DateTimeField()
    active = models.BooleanField(default=False)
    hot = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    avg_rating = models.FloatField(blank=True, null=True)
    view_count = models.FloatField(blank=True, null=True)
    rating_count = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class ArticleMedia(NewsSiteBaseModel):
    article = models.ForeignKey(Article)
    category = models.CharField(max_length=255)
    url = models.URLField()

    def __unicode__(self):
        return "%s > %s" % (self.article, self.category)


# TODO: add reference to User model
class ArticleRating(NewsSiteBaseModel):
    article = models.ForeignKey(Article)
    rating = models.FloatField()

    def __unicode__(self):
        return "%s -> %s" % (self.article, self.rating)


class RelatedArticle(NewsSiteBaseModel):
    source = models.ForeignKey(Article, related_name="source_article")
    related = models.ForeignKey(Article, related_name="related_article")
    score = models.FloatField()

    def __unicode__(self):
        return "%s -> %s" % (self.source, self.related)

# TODO: Implement both a Generic {Trending Based} feed generation artcle
# or a Personalized one based on ArticleRating


class Feed:
    pass
