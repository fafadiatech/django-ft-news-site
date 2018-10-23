import json
import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from news_site.models import Article, Source, Category
from pprint import pprint


class Command(BaseCommand):
    help = 'Clear complete database'

    def handle(self, *args, **options):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        user_file = BASE_DIR + '/commands/news.json'
        with open(user_file) as f:
            expert_data = json.load(f)
            for i in expert_data['articles']:
                title = i["title"]
                blurb = i["full_text"]
                source_url = i["source_url"]
                url_to_image = i["urlToImage"]
                published_on = i["published_on"]
                category = i["categories"]
                news_source = Source.objects.filter(name=i["source"]).first()
                if news_source:
                    news_source = news_source
                else:
                    news_source = Source.objects.create(name=i["source"])

                category, created = Category.objects.get_or_create(
                    name=i["categories"])
                print title
                Article.objects.create(
                    source=news_source, title=title,
                    blurb=blurb, source_url=source_url,
                    cover_image=url_to_image, published_on=published_on,
                    category=category)
