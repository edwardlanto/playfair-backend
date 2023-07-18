from .models import *
from rest_framework.response import Response
from playfairauth.models import CustomUserModel, CustomUserProfile 
from playfairauth.serializers import BaseUserProfileSerializer
from candidate.models import AppliedJob
from .models import Message
from playfairauth.models import Contractor
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request, pk):
    try:
        application = AppliedContract.objects.filter(id=pk).first()
        conversation = Conversation.objects.get(applied_contract=application.id)
        messages = Message.objects.filter(conversation_id=conversation.id).order_by('created_date')
        contractor = Contractor.objects.get(id=application.contractor.id)
        current_user = CustomUserModel.objects.select_related('custom_').filter(id=contractor.user.id).values('image', 'username', 'first_name', 'id', 'first_name', 'last_name').first()
        user = current_user
        user['title'] = CustomUserProfile.objects.filter(user=contractor.user.id).first().title
        # if cache.get("conversation-{pk}"):
        #     conversation = cache.get("conversation-{pk}")
        # else:
        #     conversation = ConversationSerializer(Conversation.objects.get(id=pk)).data
        #     cache.set("conversation-{pk}", conversation)
        # if cache.get("messages-{pk}"):
        #     messages = Message.objects.filter(conversation_id=pk).order_by('created_date')
        # else:
        #     messages = Message.objects.filter(conversation_id=pk).order_by('created_date')
        #     cache.set("messages-{pk}", conversation)
        return Response({
            "conversation": ConversationSerializer(conversation).data,
            "messages": MessageSerializer(messages, many=True).data,
            "current_user": user,
            # 'title': profile
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    try:
        conversation = Conversation.objects.get(applied_contract=request.data['applied_contract'])
        message = Message.objects.create(
            conversation_id=conversation,
            content=bleach.clean(request.data['content']),
            from_user=request.user
        )
        message.save()
        return Response({
          "message": message.content
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
