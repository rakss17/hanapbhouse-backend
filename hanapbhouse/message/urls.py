from django.urls import path
from . import views

urlpatterns = [
    path('conversation/', views.ConversationView.as_view(), name='conversation'),
    path('all-conversation/', views.AllConversationView.as_view(), name='all-conversation'),
]