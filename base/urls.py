from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('posts/', views.posts, name="posts"),
    path('post/create/', views.postCreate, name="post_create"),
    path('posts/search/', views.search_posts, name="search_posts"),
    path('post/update/<int:pk>', views.postUpdate, name="post_update"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]