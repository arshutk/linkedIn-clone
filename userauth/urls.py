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
    path('account/verify/', views.OTPVerificationView.as_view()),
    
    #OTP
    path('otp/resend/', views.OTPSend.as_view()),
    
    #Password Reset
    path('password/reset/', views.OTPSend.as_view()),
    path('password/reset/otp/verify/', views.OTPVerificationView.as_view()),
    path('password/reset/new_password', views.UserCreateView.as_view()),
    
    
    path('profile/<int:profile_id>/', views.UserProfileView.as_view()),
    
    #Follow
    # path('follow/<int:profile_id>/', views.FollowView.as_view()),
    
    #Connection
    # path('send/connection/<int:receiver_id>/', views.ConnectionSenderView.as_view()),
    
    # path('delete/connection/<int:connection_id>/', views.ConnectionDeleteView.as_view()),
    
    # path('view/pending_connection/', views.PendingConnectionRequestView.as_view()),
    
    # path('view/network/', views.NetworkView.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)