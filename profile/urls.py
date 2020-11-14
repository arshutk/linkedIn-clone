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

urlpatterns = [
    
    url(r'', include(router.urls)),
    path('strength/', views.ProfileStrengthView.as_view()),
    path('dashboard/', views.DasboardView.as_view()),
    path('banner/', views.BasicInfoView.as_view()), 
    path('get_work/', views.GetWorkView.as_view()),
    path('get_academic/', views.GetAcademicView.as_view()),
    path('skills/', views.SkillView.as_view()),
    path('skills/<int:skill_id>/', views.SkillUpdateView.as_view()),
    path('update/<int:profile_id>/', views.UserProfileUpdate.as_view()),
    path('view/social_profile/', views.SocialProfileView.as_view()),
    path('update/social_profile/<int:profile_id>/', views.SocialProfileUpdate.as_view()),
    path('update/banner/<int:profile_id>/', views.BannerUpdateView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)