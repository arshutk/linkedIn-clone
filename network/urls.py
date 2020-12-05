from django.urls import path, include

from network import views

from django.conf.urls.static import static

from django.conf.urls import url



urlpatterns = [
    
    #Follow
    path('follow/<int:profile_id>/', views.FollowView.as_view()),
    
    #Connection
    path('send/connection/<int:receiver_id>/', views.ConnectionSenderView.as_view()),
    
    path('delete/connection/<int:connection_id>/', views.ConnectionDeleteView.as_view()),
    
    path('view/pending_connection/', views.PendingConnectionRequestView.as_view()),
    
    path('view/connections/', views.NetworkView.as_view()),
    
    path('view/archived/request/', views.NetworkView.as_view()),
    
] 