from django.conf.urls import url

from django.urls import path, include

from rest_framework import routers

from post import views 

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('strength/<int:profile_id>/', views.ProfileStrength.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

