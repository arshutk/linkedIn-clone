from django.conf.urls import url

from django.urls import path, include, re_path

from chat import views 

from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
    path('<receiver_id>/', views.ChatView.as_view()),
    path('delete/<chat_id>', views.ChatDeleteView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

