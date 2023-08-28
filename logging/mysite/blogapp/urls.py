"""
Пути подключения для представлений приложения mapiapp.
"""

from django.urls import path
from .views import (
    ArticleListView,
    ArticleCreateView,
    ArticleDetailsView,
    ArticleUpdateView,
    ArticleDeleteView,
    )


app_name = 'blogapp'


urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleDetailsView.as_view(), name='article_details'),
    path("article/<int:pk>/update/", ArticleUpdateView.as_view(), name="article_update"),
    path('article/<int:pk>/archive/', ArticleDeleteView.as_view(), name='article_delete'),
]