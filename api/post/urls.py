from django.conf.urls import url

from django.urls import path, include, re_path

from rest_framework import routers

from post import views 

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create/', views.PostView.as_view()),
    
    path('view/<str:profile_id>/', views.GetPostView.as_view()),
   
    path('vote/<int:post_id>/<str:vote_type>/', views.VotePostView.as_view()),
    path('vote/view/<int:post_id>/', views.VoteGetView.as_view()),

    path('bookmark/<int:post_id>/', views.BookmarkView.as_view()),
    path('bookmark/view/<int:user_id>/', views.GetBookmarks.as_view()),
    
    # Comment
    path('comment/create/', views.CommentPostView.as_view()),
    path('comment/update/<int:comment_id>/', views.CommentUpdateView.as_view()),
    path('comment/like/<int:comment_id>/', views.CommentUpdateView.as_view()),
    
    # Replies
    path('comment/reply/create/', views.ReplyPostView.as_view()),
    path('comment/reply/update/<int:reply_id>/', views.ReplyUpdateView.as_view()),
    path('comment/reply/like/<int:reply_id>/', views.ReplyUpdateView.as_view()),
    
    path('feed/', views.FeedView.as_view()),
    
    #search
    path('', views.PostSearchView.as_view()),
    
    path('hashtags/', views.HashtagView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

