from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('me/', views.UserProfileView.as_view(), name='user-profile-view'),
    path('activation/<uidb64>/<token>/', views.activate_account, name='activate_account'),
]