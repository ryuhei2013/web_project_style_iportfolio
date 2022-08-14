"""Defines URL patterns for users"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    # デフォルトの認証URLを含めます。
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    # 登録ページ
    path('register/', views.register, name='register'),
]
