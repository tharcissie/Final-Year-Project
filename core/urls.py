from django.urls import path, include
from .views import *




urlpatterns = [

    path('', homepage, name='homepage'),    
    path('article/<int:pk>/details', article_details, name='detail_articles'),





    path('announcement-details/<int:pk>/', announcement_detail, name='announcement_detail'),    ### viewing the details of article at the home page

    #path('tag/<slug>/',TagListView.as_view(), name='tagged'),
    path('details/<int:pk>/like/', ArticleLikeToggle.as_view(), name='like_toggle'), #like path
    path('details/<int:pk>/dislike/', ArticleDislikeToggle.as_view(), name='dislike_toggle'),#dislike path









    path('search_result/', SearchResult.as_view(), name='search_result'),   ## path to search results view
    path('articles/cst', cst, name='cst'),          ## viewing all articles from cst
    path('articles/cbe', cbe, name='cbe'),          ## viewing all articles from cbe
    path('articles/cmhs', cmhs, name='cmhs'),       ## viewing all articles from cmhs
    path('articles/ce', ce, name='ce'),             ## viewing all articles from ce
    path('articles/cass', cass, name='cass'),       ## viewing all articles from cass
    path('articles/cavm', cavm, name='cavm'),       ## viewing all articles from cavm


    path('view/<int:pk>/like/', ArticleLikeToggle.as_view(), name='like_toggle'), #like path
    path('view/<int:pk>/dislike/', ArticleDislikeToggle.as_view(), name='dislike_toggle'),#dislike path

    
 
 ]