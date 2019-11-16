"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from website import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name="article_list"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.settings_view, name="settings"),
    path("content-editor/", views.main_editor_view, name="main_editor"),
    path("content-editor/category/<str:category>",
         views.category_main_editor_view, name="category_main_editor"),
    path("content-editor/<slug:slug>",
         views.article_editor_view, name="article_editor"),
    path("category-editor/", views.category_editor_view, name="category_editor"),
    path('articles/', views.ArticleListView.as_view(), name="article_list"),
    path('articles/category/<str:category>/',
         views.CategoryArticleListView.as_view(), name="cat_article_list"),
    path('articles/<slug:slug>/',
         views.ArticleDetailView.as_view(), name="article_detail"),
    path('admin/', admin.site.urls),
    path('download-blogposts/', views.download_blogposts,
         name="download_blogposts"),
    path('delete-blogposts/', views.delete_blogposts, name="delete_blogposts"),
    path('upload-blogposts/', views.upload_blogposts, name="upload_blogposts"),
    path('download-aws-media/', views.download_aws_media,
         name="download_aws_media"),
    path('upload-aws-media/', views.upload_aws_media,
         name="upload_aws_media"),
    path('delete-aws-media/', views.delete_aws_media,
         name="delete_aws_media"),
    url(r'^froala_editor/', include("froala_editor.urls")),
    url(r"^upload_file$", views.upload_file, name="upload_file"),
    url(r"^upload_file_validation", views.upload_file_validation,
        name="upload_file_validation"),
    url(r"^upload_image$", views.upload_image, name="upload_image"),
    url(r"^upload_image_validation", views.upload_image_validation,
        name="upload_image_validation"),
    url(r"^upload_video$", views.upload_video, name="upload_video"),
    url(r"^upload_video_validation", views.upload_video_validation,
        name="upload_video_validation"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_DIR)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
