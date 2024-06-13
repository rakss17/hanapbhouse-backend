from django.urls import path
from . import views

urlpatterns = [
    path('coversation/', views.ConversationView.as_view(), name='coversation'),
]