from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from playfairauth.models import CustomUserModel
from .filters import ContractFilter
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from .models import Contract
from django.contrib.auth.models import User
from datetime import date
from .serializers import * 
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from chat.models import Conversation, ConversationMember
from django.db.models import Q
from django.db import transaction
import bleach
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.conf import settings
from company.models import Company
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)
bleached_tags = ['p', 'b', 'br', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'em', 'a', 'div', 'strong']
bleached_attr = ['class', 'href', 'style']

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
    
@api_view(['GET'])
def index(request):
    try:
        # cache.delete('cached_contracts')
        page = request.GET.get('page', '1')
        per_page = 50
        # if page == '1':
        #     cached_page = cache.get('cached_contracts')
        #     serialized = BaseContractSerializer(cached_page, many=True,  context={'request': request}).data
        #     count = len(serialized)
        #     if cached_page:
        #         return Response({
        #             'count': count,
        #             'per_page': per_page,
        #             'contracts': serialized
        #         }, status=status.HTTP_200_OK)

        order = "-created_date"
        filterset = ContractFilter(request.GET, queryset=Contract.objects.all().order_by(order)).qs
        count = filterset.count()
        cache.set('cached_contracts', filterset)
        paginator = Paginator(filterset, per_page)
        paginator = paginator.page(page)
        serializer = BaseContractSerializer(paginator, many=True,  context={'request': request})

        return Response({
            "count": count,
            "per_page": per_page,
            'contracts': serializer.data
        }, status=status.HTTP_200_OK)
    
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist as e:
        return Response(status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)},status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def verify(request):
    try:
        user = request.user

        if user.gig_verified == False:
            return Response({"verified": False},status=status.HTTP_200_OK)
        else:
            return Response({"verified": True},status=status.HTTP_200_OK) 
    
    except ObjectDoesNotExist as e:
        return Response(status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create(request):
    try:
        company = Company.objects.filter(user=request.user).first()
        data = request.data
        contract = Contract.objects.create(
            title = bleach.clean(data['title']),
            company=company,
            description= bleach.clean(data['description'], attributes=bleached_attr, tags=bleached_tags),
            currency = data['currency'],
            amount = data['amount'],
            delivery_type = bleach.clean(data['delivery_type']),
            quantity = data['quantity'],
            type = bleach.clean(data['type']),
            lat = data['lat'],
            user = request.user,
            long = data['long'],
            min_rate = data['min_rate'],
            max_rate = data['max_rate'],
            city = bleach.clean(data['city']),
            state = bleach.clean(data['state']),
            country = bleach.clean(data['country']),
            buyer = request.user
        )
        contract.save()
        
        return Response({'contract': ContractSerializer(contract).data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@transaction.atomic
def update(request):
    try:
        data = request.data
        contract = Contract.objects.create(
            title = bleach.clean(data['title']),
            description= bleach.clean(data['description'], attributes=bleached_attr, tags=bleached_tags),
            currency = data['currency'],
            amount = data['amount'],
            delivery_type = bleach.clean(data['delivery_type']),
            quantity = data['quantity'],
            type = bleach.clean(data['type']),
            lat = data['lat'],
            long = data['long'],
            min_rate = data['min_rate'],
            max_rate = data['max_rate'],
            city = bleach.clean(data['city']),
            state = bleach.clean(data['state']),
            country = bleach.clean(data['country']),
            buyer = request.user
        )
        contract.save()
        
        return Response({'contract': ContractSerializer(contract).data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@transaction.atomic
def get(request, pk):
    try:
        contract = get_object_or_404(Contract, id=pk)
        serializer = ContractSerializer(contract, many=False, context={'request': request}).data
        # candidates = job.appliedjob_set.all().count()
        
        # relatedJobs = JobSerializer(Job.objects.filter(industry=serializer.data['industry']).exclude(id=pk), many=True)

        return Response({
            "contract": serializer,
            # "related": relatedJobs.data,
            # "candidates": candidates,
        }, status=status.HTTP_200_OK)
    
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
