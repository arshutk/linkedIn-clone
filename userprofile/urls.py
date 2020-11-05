from django.conf.urls import url

from django.urls import path, include

from django.conf.urls import url

from rest_framework import routers

from userprofile import views 


router = routers.DefaultRouter()
router.register(r'work/', views.WorkExperienceViewset)
router.register(r'education/', views.EducationViewset)


urlpatterns = [
    url(r'^', include(router.urls)),
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
] 