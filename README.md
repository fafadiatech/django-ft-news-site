# Django FT News-site

This is a re-usable News Site Application for use in Django projects

## Authors

- Prasen Revankar {prasen@fafadiatech.com}
- Sidharth Shah {sidharth@fafadiatech.com}

## Feature Supported

1. Aggregate News from Multiple Sites
    1. Bloomberg
    1. CNN Money
    1. The Verge
    1. Tech Crunch
    1. The Register
    1. Fast Company
    1. BBC
    1. NY Times
    1. Huffington Post
    1. The Guardian
1. APIs
1. Easy to Browse
1. Content Recommendation
1. Email Digest
1. Auto Complete
1. Search
1. Advanced Search

## Architecture

1. Web Framework
    - Django {Possibly Python 3}
    - Django Rest Framework for APIs
1. DB
    - Postgres
1. Data Ingestion Pipeline
    - Crawler written in Colly {which is a Golang Library}
1. Indexer
    - Apache Solr 7 Series

## Bonus Goal

1. Build a Text Summarization Script