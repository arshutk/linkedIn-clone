from django.urls import path,include

from userauth import views

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Sign-UP
    path('create/', views.UserCreateView.as_view()),
    path('create/profile/<int:user_id>/', views.UserProfileCreateView.as_view()),
    path('account/verify/', views.AccountVerificationView.as_view()),
    
    #OTP
    path('otp/resend/', views.OTPResend.as_view()),
    
    
    path('profile/<int:profile_id>/', views.UserProfileView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)