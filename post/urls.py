from django.conf.urls import url

from django.urls import path, include

from rest_framework import routers

from post import views 

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create/', views.PostView.as_view()),
    path('vote/view/<int:post_id>/', views.VoteGetView.as_view()),
    path('vote/<int:post_id>/<str:vote_type>/', views.VotePostView.as_view()),
    path('bookmark/create/<int:post_id>/', views.BookmarkView.as_view()),
    path('bookmark/view/<int:user_id>/', views.GetBookmarks.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

