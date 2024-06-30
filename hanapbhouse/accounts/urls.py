from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('me/', views.UserProfileRetrieveUpdateView.as_view(), name='user-profile-view'),
]