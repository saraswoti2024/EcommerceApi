from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name="registerview"),
    path('verifyotp/',VerifyOtp.as_view(),name="verifyotp"),
    path('profile/',Profile.as_view(),name="profile"),
    path('api/token/',CustomToken.as_view(), name='token_obtain_pair'),
]