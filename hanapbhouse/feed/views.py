from rest_framework import generics
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feed, SavedFeed
from .serializers import FeedSerializer, SavedFeedSerializer
from accounts.models import User
from property.models import Property
from utils.permissions import IsOwnerOrReadOnly

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
        queryset = Feed.objects.all().exclude(owner=self.request.user)

        if category and category != "All":
            queryset = queryset.filter(Q(content__type__icontains=category))

        if street_3 and city:
            queryset = queryset.filter(Q(content__address__street_3__icontains=street_3) & 
                                       Q(content__address__city__icontains=city))
        elif street_3:
            queryset = queryset.filter(Q(content__address__street_3__icontains=street_3))
        elif city:
            queryset = queryset.filter(Q(content__address__city__icontains=city))
            
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
    
class FeedUpdateDetailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():

            new_image = request.FILES.get('image', None)
        
            if new_image:

                if instance.image:
                    instance.image.delete()

                instance.image = new_image
            else:
                
                if instance.image:
                    instance.image.delete()

            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

class VisitFeedByUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedSerializer

    def list(self, request, *args, **kwargs):
        owner = request.query_params.get('owner')

        timezone.activate('Asia/Manila')
        queryset = Feed.objects.filter(owner=owner)

        page_size = 10
        page_number = request.query_params.get('page', 1)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = self.serializer_class(page_obj.object_list, many=True)

        return Response({
            'feed_data': serializer.data,
            'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
        }, status=200)
    
class SavedFeedCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedFeedSerializer

    def get_queryset(self):
        return SavedFeed.objects.filter(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        owner = request.data.get('owner')
        content = request.data.get('content')

        owner_instance = User.objects.get(id=owner)
        feed_instance = Feed.objects.get(id=content)
        SavedFeed.objects.create(
            owner=owner_instance,
            content=feed_instance,
        )

        return Response({"message": "Saved successfully"}, status=201)\
        
class UnsavedFeedView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedFeedSerializer
    queryset = SavedFeed.objects.all()

    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Unsaved successfully"}, status=200)