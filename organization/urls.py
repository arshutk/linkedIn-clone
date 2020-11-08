from django.conf.urls import url

from django.urls import path, include

from django.conf.urls import url

from rest_framework import routers

from organization import views 

from django.conf import settings

from django.conf.urls.static import static


# router = routers.DefaultRouter()
# router.register(r'work/', views.WorkExperienceViewset)
# router.register(r'education/', views.EducationViewset)


urlpatterns = [
    # url(r'^', include(router.urls)),
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)