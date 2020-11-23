from django.conf.urls import url

from django.urls import path, include

from rest_framework import routers

from notification import views 

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('get/notification/<int:profile_id>/', views.GetNotificationView.as_view()),
        
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)