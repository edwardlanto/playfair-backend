from .models import *
from rest_framework.response import Response
from playfairauth.models import CustomUserModel, CustomUserProfile 
from playfairauth.serializers import BaseUserProfileSerializer
from candidate.models import AppliedJob
from .models import Message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from company.models import Company, SavedCompanies
import bleach
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

    #   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", null=True)
    # from_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="from_user", null=True)
    # content = models.CharField(null=True)
    # created_date = models.DateTimeField(auto_now_add=True)
@api_view(['GET'])
def get_conversation(request, pk):
    try:
        conversation = Conversation.objects.get(id=pk)
        conversation = ConversationSerializer(conversation).data
        messages = Message.objects.filter(conversation_id=pk).order_by('created_date')
        # messages = MessageSerializer(messages).data
        return Response({
            "conversation": conversation,
            "messages": MessageSerializer(messages, many=True).data
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_message(request):
    try:
        conversation = Conversation.objects.get(id=request.data['conversation'])
        message = Message.objects.create(
            conversation_id=conversation,
            content=request.data['content'],
            from_user=request.user
        )
        message.save()
        # messages = MessageSerializer(messages).data
        return Response({
            "message": 'success'
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
