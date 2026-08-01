from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterAPIView,LoginAPIView,ProfileAPIView,LogoutAPIView,ChangePasswordAPIView


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("logout/",LogoutAPIView.as_view(),name="logout"),
    path("change-password/",ChangePasswordAPIView.as_view(),name="change_password"),
]