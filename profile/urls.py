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
router.register(r'vacancy', views.JobVacancyView)

urlpatterns = [
    
    url(r'', include(router.urls)),
    path('strength/', views.ProfileStrengthView.as_view()), 
    path('dashboard/<int:profile_id>/', views.DasboardView.as_view()),
    path('banner/<int:profile_id>/', views.BannerView.as_view()), 
    path('get_work/<int:profile_id>/', views.GetWorkView.as_view()),
    path('get_academic/<int:profile_id>/', views.GetAcademicView.as_view()),
    path('skills/<int:profile_id>/', views.SkillView.as_view()),
    path('skills/update/<int:skill_id>/', views.SkillUpdateView.as_view()),
    path('skills/endorse/<int:skill_id>/', views.SkillEndorsementView.as_view()),

    path('view/social_profile/', views.SocialProfileView.as_view()),

    path('banner/update/<int:profile_id>/', views.BannerUpdateView.as_view()),
    path('about/update/<int:profile_id>/', views.BannerUpdateView.as_view()),
    
    path('vacancy/apply/<int:vacancy_id>/', views.VacancyApplyView.as_view()),
    path('view/vacancy/applied/vacancy/', views.AppliedVacancyGetView.as_view()),
    path('vacancy/bookmark/<int:vacancy_id>/', views.VacancyBookmarkView.as_view()),
    path('vacancy/bookmark/view/', views.VacancyBookmarkGetView.as_view()),
    path('vacancy/review/<int:vacancy_id>/<applicant_id>/', views.VacancyReviewView.as_view()),
    
    path('view/recommended/vacancy/', views.VacancyRecommendView.as_view()),
    
    #search
    path('search/', views.JobSearchView.as_view()),
        
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)