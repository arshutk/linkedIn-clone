from django.urls import path,include

from userauth import views

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url

urlpatterns = [

    path('', views.UserCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.UserRetrieveUpdateDeleteView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)