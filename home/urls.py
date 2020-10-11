from django.urls import path
from .views import *





urlpatterns = [
    path('', homepage, name='homepage'),          ### path to home view (home page)
    path('article-details/<int:pk>/', article_details, name='detail_articles'),    ### viewing the details of article at the home page

    path('announcement-details/<int:pk>/', announcement_detail, name='announcement_detail'),    ### viewing the details of article at the home page

    #path('tag/<slug>/',TagListView.as_view(), name='tagged'),
    path('details/<int:pk>/like/', ArticleLikeToggle.as_view(), name='like_toggle'), #like path
    path('details/<int:pk>/dislike/', ArticleDislikeToggle.as_view(), name='dislike_toggle'),#dislike path

]