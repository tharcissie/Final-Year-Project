from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from .views import *




urlpatterns = [
    path('', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('dashboard/', dashboard, name='dashboard'),

    path('create-article/', article_create, name='create_article'),
    path('my-articles/', my_articles, name='my_articles'),
    path('article-details/<int:pk>/', article_detail, name='article_details'),
    path('edit-article/<int:pk>', edit_article, name='edit_article'),


    path('update_profile/', update_profile, name='update_profile'),

    path('all-announcements/',all_announcements,name='all_announcements'),
    path('all-published-articles/',published_articles,name='all_published_articles'),
    path('all-users/',all_users,name='all_users'),
    path('all-subscribers/',all_subscribers,name='all_subscribers'),


    # new

    path('users/',users,name='users'),
    path('subscribers/',subscribers,name='subscribers'),

    path('cst-articles/',cstArticles,name='cstArticles'),
    path('cbe-articles/',cbeArticles,name='cbeArticles'),
    path('cmhs-articles/',cmhsArticles,name='cmhsArticles'),
    path('cass-articles/',cassArticles,name='cassArticles'),
    path('cavm-articles/',cavmArticles,name='cavmArticles'),
    path('ce-articles/',ceArticles,name='ceArticles'),

    path('article/details/<int:pk>/', articleDetails, name='articleDetails'),
    path('delete-article/<int:pk>', delete_article, name='delete_article'),

    path('new-announcement/',new_announcement,name='new_announcement'),
    path('announcements/',announcements,name='announcements'),

    path('settings/password/', change_password, name='change_password'),

 ]