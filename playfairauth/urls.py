from django.urls import path, include
from .views import  GoogleSocialAuthView, FacebookSocialAuthView, CandidateView, EmployerView
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from .views import *

urlpatterns = [
    path('geo-location/', views.get_geo_location),
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
    path('login/', LoginView.as_view(), name='custom_login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register-candidate/', CandidateView.as_view()),
    path('logo/', views.get_logo, name='get-logo'),
    path('get-me/', views.get_me, name='get-me'),
    path('register-company/credentials/', EmployerView.as_view()),
    path('register-candidate/credentials/', view=views.register_candidate_credentials, name="register-candidate-credentials"),
    path('profile/me/', views.me, name='me'),
    path('profile/resume/', views.resume, name='resume'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('is-candidate/', views.get_is_candidate, name='getIsCandidate'),
    path('is-employer/', views.get_is_employer, name='getIsEmployer'),
    path('csrf/', views.getCsrf, name='get_csrf'),
    path('forgot-password-request/', views.forgot_password, name='reset_password'),
    path('check-password-reset/', views.check_password_reset, name='check_password_reset'),
    path('forgot-password-reset/', views.password_reset_done, name='password_reset_done'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('check-is-complete/', views.check_is_complete, name='check_is_complete')
]

# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']