from django.urls import path, include
from . import views

urlpatterns = [
    path('property-creation-listing/', views.PropertListCreateView.as_view(), name='property-creation-listing')
]