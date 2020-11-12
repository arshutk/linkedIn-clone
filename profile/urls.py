from django.conf.urls import url

from django.urls import path, include

from rest_framework import routers

from profile import views 

from django.conf import settings
from django.conf.urls.static import static

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
    path('strength/', views.ProfileStrengthView.as_view()),
    path('dashboard/', views.DasboardView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)