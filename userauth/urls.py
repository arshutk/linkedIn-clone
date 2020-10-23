from django.urls import path,include

from userauth import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.UserView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)