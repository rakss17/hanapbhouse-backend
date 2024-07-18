from rest_framework import generics
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, F, Q
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer
from .models import Message

class ConversationView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        room_name = request.query_params.get('room_name')

        timezone.activate('Asia/Manila')
        queryset = Message.objects.filter(room_name=room_name)

        queryset = queryset.order_by('-send_timestamp')
        page_size = 10
        page_number = request.query_params.get('page_number', 1)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = self.serializer_class(page_obj.object_list, many=True)

        return Response({
            'message_data': serializer.data,
            'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
        }, status=200)

class AllConversationView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user

        # Subquery to get the latest message for each sender-receiver pair
        latest_messages = Message.objects.filter(
            Q(sender=OuterRef('sender'), receiver=OuterRef('receiver')) |
            Q(sender=OuterRef('receiver'), receiver=OuterRef('sender'))
        ).order_by('-send_timestamp').values('id')[:1]

        # Filter messages where the user is either the sender or the receiver
        queryset = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).annotate(
            latest_message_id=Subquery(latest_messages)
        ).filter(
            id=F('latest_message_id')
        )

        queryset = queryset.order_by('-send_timestamp')
        page_size = 10
        page_number = request.query_params.get('page_number', 1)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = self.serializer_class(page_obj.object_list, many=True)

        return Response({
            'message_data': serializer.data,
            'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
        }, status=200)