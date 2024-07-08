from django.urls import path
from . import views

urlpatterns = [
    path('feed-creation-listing/', views.FeedListCreateView.as_view(), name='feed-creation-listing'),
    path('public-feed-listing/', views.PublicFeedListView.as_view(), name='public-feed-listing'),
    path('is-feed-saved/', views.IsFeedSavedView.as_view(), name='is-feed-saved'),
    path('saved-feed-creation-listing/', views.SavedFeedCreateView.as_view(), name='saved-feed-creation-listing'),
    path('unsaved-feed/<str:pk>/', views.UnsavedFeedView.as_view(), name='unsaved-feed'),
    path('feed-update-details/<str:pk>/', views.FeedUpdateDetailView.as_view(), name='feed-update-details'),
    path('visit-feeds-by-user-listing/', views.VisitFeedByUserView.as_view(), name='visit-feeds-by-user-listing'),
]