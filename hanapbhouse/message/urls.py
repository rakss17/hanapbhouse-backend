from django.urls import path
from . import views

urlpatterns = [
    path('coversation/', views.ConversationView.as_view(), name='coversation'),
    path('all-conversation/', views.AllConversationView.as_view(), name='all-conversation'),
]