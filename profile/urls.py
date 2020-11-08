from django.conf.urls import url

from django.urls import path, include

from django.conf.urls import url

from rest_framework import routers

from profile import views 


router = routers.DefaultRouter()
router.register(r'work', views.WorkExperienceViewset)
router.register(r'education', views.EducationViewset)
router.register(r'certification', views.LicenseAndCertificationViewset)
router.register(r'volunteer', views.VolunteerExperienceViewset)
router.register(r'courses', views.CourseViewset)
router.register(r'projects', views.ProjectViewset)
router.register(r'scores', views.TestScoreViewset)
router.register(r'skills', views.SkillsViewset)


urlpatterns = [
    url(r'', include(router.urls)),
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
] 