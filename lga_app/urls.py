from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from lga_app.models import Article, Category, Comment, ArticleCreateView, ArticleUpdateView


urlpatterns = ([
    path('', views.home, name='home'),
    path('home_articles', views.home_articles, name='home_articles'),

    path('login', views.login_user, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('update_user/', views.update_user, name="update_user"),

    path('post_article/', ArticleCreateView.as_view(), name='post_article'),
    path('article/<int:pk>', views.article_detail, name='article_detail'),
    path('article_update/<int:pk>', ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<int:pk>', views.article_delete, name='article_delete'),
    path('comment_update/<int:pk>', views.comment_update, name='comment_update'),
    path('comment_delete/<int:pk>', views.comment_delete, name='comment_delete'),

    path("upload/", views.custom_upload_function, name="custom_upload_file"),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor5_upload_file"),

]
               )