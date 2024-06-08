from django.urls import path
from . import views

urlpatterns = [
    path('feed-creation-listing/', views.FeedListCreateView.as_view(), name='feed-creation-listing'),
    path('public-feed-listing/', views.PublicFeedListView.as_view(), name='public-feed-listing')
]