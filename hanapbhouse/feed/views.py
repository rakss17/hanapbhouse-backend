from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feed
from .serializers import FeedSerializer
from accounts.models import User
from property.models import Property

class FeedListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedSerializer

    def create(self, request, *args, **kwargs):
         # Feed data from HTTP Post Request
        owner = request.data.get('owner')
        content = request.data.get('content')
        feed_image = request.FILES.get('image')

        # Image processing
        saved_image = None

        if feed_image:
            saved_image = feed_image

        # Feed creation
        owner_instance = User.objects.get(id=owner)
        property_instance = Property.objects.get(id=content)
        Feed.objects.create(
            owner=owner_instance,
            content=property_instance,
            image=saved_image
        )

        return Response({"message": "Feed created successfully"}, status=201)