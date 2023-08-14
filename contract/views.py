from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import stripe
from candidate.serializers import *
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from playfairauth.models import CustomUserModel
from payment.models import PaymentIntent
from .filters import ContractFilter
from rest_framework.permissions import IsAuthenticated
import decimal
import math
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
from playfairauth.models import Contractor
from company.models import Company
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from candidate.models import AppliedContract
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os
stripe.api_key = os.environ.get("STRIPE_TEST_API")

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)
bleached_tags = ['p', 'b', 'br', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'em', 'a', 'div', 'strong', 'li', 'ol', 'ul']
bleached_attr = ['class', 'href', 'style']

@api_view(['GET'])
def open_chat(request, pk):
    try:
        application = get_object_or_404(AppliedContract, id=pk)
        contract = Contract.objects.get(id=application.contract.id)
        current_conversation = Conversation.objects.filter(contract=contract.id).first()
        if current_conversation:
            return Response({"thread": current_conversation.id},status=status.HTTP_200_OK)

        conversation = Conversation.objects.create(
            name=contract.title,
            contract=contract,
            last_message_user=None,
            last_message=None,
            application=application
        )
        conversation.save()
        conversation_poster = ConversationMember.objects.create(
            conversation_id=conversation,
            user=application.poster,
        )

        contractor = Contractor.objects.get(id=application.contractor.id)
        conversation_poster.save()
        conversation_contractor = ConversationMember.objects.create(
            conversation_id=conversation,
            user=contractor.user,
        )
        conversation_contractor.save()
        
        return Response({"thread": conversation.id},status=status.HTTP_200_OK)
    
    except Contract.DoesNotExist as e:
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

        order =  '-created_date' if request.GET.get('orderBy') == 'asc' else 'created_date'
        filterset = ContractFilter(request.GET, queryset=Contract.objects.all().order_by(order)).qs
        count = filterset.count()
        cache.set('cached_contracts', filterset)
        paginator = Paginator(filterset, per_page)
        paginator = paginator.page(page)
        serializer = BaseContractSerializer(paginator, many=True,  context={'request': request})

        return Response({
            "count": count, 
            "per_page": per_page,
            'contracts': serializer.data,
            'candidates': []
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
            user = request.user,
            long = data['long'],
            min_rate = data['min_rate'],
            max_rate = data['max_rate'],
            city = bleach.clean(data['city']),
            state = bleach.clean(data['state']),
            country = bleach.clean(data['country']),
            poster = request.user
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
        user = request.user
        serializer = ContractSerializer(contract, many=False, context={'request': request}).data
        related_contracts = ContractSerializer(Contract.objects.filter(industry=serializer['industry']).exclude(id=pk), many=True, context={'request': request}).data
        groups = []
        
        for g in request.user.groups.all():
            groups.append(g.name)
        
        return Response({
            "contract": serializer,
            "related_contracts": related_contracts,
            "groups": groups,

        }, status=status.HTTP_200_OK)
    
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def apply(request, pk):
    try:
        with transaction.atomic():
            user = request.user
            data = request.data
            contractor = Contractor.objects.filter(user=user).first()
            contract = get_object_or_404(Contract, id=pk)

            already_applied = AppliedContract.objects.filter(contract=contract, user=user).exists()
            if already_applied:
                return Response({ "message": "You have already applied for this job"}, status=status.HTTP_200_OK)
            
            applied = AppliedContract.objects.create(
                contract=contract,
                amont=contract.amount,
                contractor=contractor,
                poster=contract.poster,
                user=user,
                coverLetter= bleach.clean(data['coverLetter'], tags=bleached_tags)
            )
            applied.save()

            return Response({"message": "Successfully applied"}, status=status.HTTP_200_OK)
    except Contract.DoesNotExist:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, pk):
    try:
        contract = get_object_or_404(Contract, id=pk)
        contract.delete()

        return Response({'contract': contract.id}, status=status.HTTP_200_OK)
    except Contract.DoesNotExist:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def managed_contracts(request):
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
        candidates = []
        for contract in paginator:
            candidates.append(AppliedContract.objects.filter(contract=contract).values().count())

        return Response({
            "count": count,
            "per_page": per_page,
            'contracts': serializer.data,
            'candidates': candidates
        }, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def approve_contract(request, pk, user):
#     try:
#         return Response(status=status.HTTP_200_OK)
    
#     except Exception as e:
#         return Response(status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def delete_contract(request, pk):
#     try:
#         return Response(status=status.HTTP_200_OK)
    
#     except Exception as e:
#         return Response(status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pause_contract(request, pk):
    try:
        return Response(status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def applications(request):
    try:
        if request.method == 'GET':
            user = request.user
            contracts = Contract.objects.values('id', 'title', 'delivery_type', 'amount', 'city', 'state', 'country', 'user', 'contractor').filter(user=user, is_active=True)

            for c in contracts:
                c['applications'] = BaseAppliedContractSerializer(AppliedContract.objects.filter(contract=c['id']), many=True).data

            return Response({'contracts': contracts}, status=status.HTTP_200_OK)
    
        if request.method == 'POST':
            return Response({'message: '},status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_200_OK)
    
        
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_application(request, pk):
    try:
        print("RAN")
        application = AppliedContract.objects.filter(id=pk).first()
        id = application.id
        application.delete()

        return Response({'application': id}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application(request, pk):
    try:
        with transaction.atomic():
            application = AppliedContract.objects.filter(id=pk).first()
            application.is_approved = request.data['is_approved']
            application.save()

            contract = Contract.objects.get(id=application.contract.id)
            current_conversation = Conversation.objects.filter(contract=contract.id).first()
            print(request.data['is_approved'])
            if current_conversation != None:
                return Response({"conversation": current_conversation.id, 'application': AppliedContractSerializer(application).data},status=status.HTTP_200_OK)
            if request.data['is_approved'] == True:
                print('true')
                conversation = Conversation.objects.create(
                    name=contract.title,
                    applied_contract=application,
                    last_message_user=None,
                    last_message=None
                )
                conversation.save()
                conversation_poster = ConversationMember.objects.create(
                    conversation_id=conversation,
                    user=contract.poster,
                )
                conversation_poster.save()

                conversation_contractor = ConversationMember.objects.create(
                    conversation_id=conversation,
                    user=contract.contractor,
                )
                conversation_contractor.save()
                return Response({'application': AppliedContractSerializer(application).data, 'conversation': conversation.id },status=status.HTTP_200_OK)

            else:
                return Response({'application': AppliedContractSerializer(application).data, 'conversation': None},status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def approve_application(request):
    try:
        user = request.user
        contracts = Contract.objects.filter(user=user).values('id', 'title', 'delivery_type', 'amount', 'city', 'state', 'country')
        for c in contracts:
            c['applications'] = BaseAppliedContractSerializer(AppliedContract.objects.filter(contract=c['id']), many=True).data

        return Response({'contracts': contracts}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def application_total(request, pk):
    if request.method == 'POST':
        application = None
        return Response({'application': application}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        try:
            application = AppliedContract.objects.get(id=bleach.clean(pk))
            sub_total = application.amount * 100
            stripe_fee = int(application.amount) * 0.089 + 0.30
            stripe_fee = math.trunc(stripe_fee * 100)
            currency = Contract.objects.get(id=application.contract.id).currency
            total = sub_total + stripe_fee
            if application.payment_intent == None:
                instance = stripe.PaymentIntent.create(
                    amount=total,
                    currency=currency['currencyCode'],
                    automatic_payment_methods={"enabled": True},
                )
                application.payment_intent = instance.id
                application.save()

                return Response({
                    'payment_intent': instance,
                    'total': total, 
                    'sub_total': application.amount, 
                    'service_fee': stripe_fee, 'currency': currency
                }, status=status.HTTP_200_OK)
            else:
                instance = stripe.PaymentIntent.retrieve(
                    application.payment_intent,
                )
                return Response({
                    'payment_intent': instance,
                    'total': total, 
                    'sub_total': application.amount, 
                    'service_fee': stripe_fee, 'currency': currency
                }, status=status.HTTP_200_OK)
                
        except AppliedContract.DoesNotExist:
            return Response({"error": "Could not find Application"}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
def paid_application(request, application):
    try:
        application = AppliedContract.objects.get(id=application)
        contract = Contract.objects.get(id=application.contract.id)

        if application.poster != request.user:
            return Response({"error": "Can not update resource"}, status=status.HTTP_401_UNAUTHORIZED)            

        contract.paid = True
        contract.status = 'In Progress'
        application.status = 'In Progress'
        contract.save()
        return Response({'message successfully'},status=status.HTTP_200_OK)
    except AppliedContract.DoesNotExist:
            return Response({"error": "Could not find Application"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    