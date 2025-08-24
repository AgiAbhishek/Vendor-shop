from django.urls import re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    re_path(r'^register/?$', RegisterView.as_view(), name='register'),
    re_path(r'^login/?$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
]
