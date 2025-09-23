from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name="registerview"),
    path('verifyotp/',VerifyOtp.as_view(),name="verifyotp"),
]