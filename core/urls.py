from django.urls import path, include
from .views import SearchResult, ArticleLikeToggle, ArticleDislikeToggle, cst, cbe, cmhs, ce, cass, cavm




urlpatterns = [

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