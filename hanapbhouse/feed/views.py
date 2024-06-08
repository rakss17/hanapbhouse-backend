from rest_framework import generics
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feed
from .serializers import FeedSerializer
from accounts.models import User
from property.models import Property

class FeedListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(owner=self.request.user)

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
    
class PublicFeedListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedSerializer

    def list(self, request, *args, **kwargs):
        street_3 = request.query_params.get('street_3')
        city = request.query_params.get('city')
        category = request.query_params.get('category')

        timezone.activate('Asia/Manila')
        queryset = Feed.objects.all()

        if category and category != "All":
            queryset = queryset.filter(Q(content__type__icontains=category))

        if street_3 and city:
            queryset = queryset.filter(Q(content__address__street_3__icontains=street_3) & 
                                       Q(content__address__city__icontains=city))
            
        queryset = queryset.order_by('timestamp')
        page_size = 10
        page_number = request.query_params.get('page', 1)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = self.serializer_class(page_obj.object_list, many=True)

        return Response({
            'feed_data': serializer.data,
            'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
        }, status=200)