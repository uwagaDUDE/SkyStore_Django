"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Sky_store.views import ProductStore, start_page, BlogListView, \
    BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, \
    BlogPostDeleteView, add_product, edit_product



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name='home'),
    path('store/', ProductStore.as_view(), name='store'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('<slug:slug>', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('create/', BlogPostCreateView.as_view(), name='create_blog_post'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='update_blog_post'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view()),
    path('new_product/', add_product, name='new'),
    path('editor/', edit_product, name='editor'),
    path('editor/<int:id>/', edit_product, name='edit_product')

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
