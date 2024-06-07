from django.urls import path, include
from . import views

urlpatterns = [
    path('feed-creation-listing/', views.FeedListCreateView.as_view(), name='feed-creation-listing')
]