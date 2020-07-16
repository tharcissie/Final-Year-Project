import django_filters
from core.models import *


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['college',]



class SubscriberFilter(django_filters.FilterSet):
    class Meta:
        model = Subscriber
        fields = ['article_category',]
