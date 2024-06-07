from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('property/', include('property.urls')),
    path('feed/', include('feed.urls'))
]