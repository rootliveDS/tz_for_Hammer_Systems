from django.urls import path
from .views import RequestAuthorizationCodeView, VerifyAuthorizationCodeView, UserProfileView

urlpatterns = [
    path('request-auth-code/', RequestAuthorizationCodeView.as_view(), name='request-auth-code'),
    path('verify-auth-code/<str:phone_number>/', VerifyAuthorizationCodeView.as_view(), name='verify-auth-code'),
    path('user-profile/<str:phone_number>/', UserProfileView.as_view(), name='user-profile'),
]