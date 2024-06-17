from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('me/', views.UserProfileRetrieveUpdateView.as_view(), name='user-profile-view'),
    path('activation/<uidb64>/<token>/', views.activate_account, name='activate_account'),
]