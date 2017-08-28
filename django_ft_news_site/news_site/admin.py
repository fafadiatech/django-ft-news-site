# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (Category, SubCategory, 
                     Industry, Source, HashTag, Article, ArticleMedia,
                     ArticleRating, RelatedArticle)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Industry)
admin.site.register(Source)
admin.site.register(HashTag)
admin.site.register(Article)
admin.site.register(ArticleMedia)
admin.site.register(ArticleRating)
admin.site.register(RelatedArticle)
