from django.urls import path

from .views import (
    RegisterCompanyView, 
    UserLoginView,
    UserProfileView
)


urlpatterns = [
    path('register/', RegisterCompanyView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('accounts/profile/', UserProfileView.as_view(), name='user_profile'),
]