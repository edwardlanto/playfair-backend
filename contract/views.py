from django.utils import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max, Count
from rest_framework.pagination import PageNumberPagination
from company.serializers import BaseCompanySerializer
from candidate.serializers import AppliedJobSerializer
from django.shortcuts import get_object_or_404
from playfairauth.models import CustomUserModel
from .filters import ContractFilter
from company.models import Company
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import JsonResponse
from .models import Contract
from django.core import serializers
from django.contrib.auth.models import User
from datetime import date
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from chat.models import Conversation, ConversationMember
from django.db.models import Q
CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

@api_view(['POST'])
def confirm_contract(request, pk):
    try:
        contract = Contract.objects.get(id=pk)
        current_conversation = Conversation.objects.filter(contract=contract.id).first()
        if current_conversation:
            return Response({"thread": current_conversation.id},status=status.HTTP_200_OK)

        conversation = Conversation.objects.create(
            name=contract.title,
            contract=contract,
            last_message_user=None,
            last_message=None
        )
        conversation.save()
        conversation_seller = ConversationMember.objects.create(
            conversation_id=conversation,
            user=contract.seller,
        )
        conversation_seller.save()
        conversation_buyer = ConversationMember.objects.create(
            conversation_id=conversation,
            user=contract.buyer,
        )
        conversation_buyer.save()
        
        return Response({"thread": conversation.id},status=status.HTTP_200_OK)
    
    except ObjectDoesNotExist as e:
        return Response(status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)},status.HTTP_400_BAD_REQUEST)

