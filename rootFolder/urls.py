from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from home.views import tagged
from core.views import ChartData, ChartData_





urlpatterns = [
    
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('articles/', include('core.urls')),

    path('api/chart/data/', ChartData.as_view()),
    path('api2/chart/data/', ChartData_.as_view()),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('tag/<slug:slug>/', tagged, name="tagged"),
    
    path('accounts/',  include('allauth.urls')),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)