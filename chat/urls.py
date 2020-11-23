from django.conf.urls import url

from django.urls import path, include, re_path

from chat import views 

from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

