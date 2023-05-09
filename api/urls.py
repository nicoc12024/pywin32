from django.urls import path
from . import views

urlpatterns = [
    path('users/create/', views.create_user, name='create_user'),  
    path('users/update/', views.update_user, name='update_user'),
    path('users/get/', views.get_user, name='get_user'),  
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/', views.get_blogs, name='get_blogs'),
    path('blogs/user/<str:user_id>/', views.get_user_posts, name='get_user_posts'),
    path('blogs/update/<int:pk>/', views.update_blog, name='update_blog'),
    path('blogs/delete/<int:pk>/', views.delete_blog, name='delete_blog'),  
    path('likes/get/', views.get_like, name='get_like'),
    path('liked_posts/', views.get_user_liked_posts, name='get_user_liked_posts'),
    path('likes/<int:pk>/', views.delete_like, name='delete-like'),
    path('likes/', views.create_like, name='create-like'),
    path('comments/create/', views.create_comment, name='create_comment'),
    path('comments/blog/<int:blog_id>/', views.get_blog_comments, name='get_blog_comments'),
    path('comments/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('users/<str:user_id>/blog_likes/', views.get_user_blog_likes, name='get_user_blog_likes')
]

