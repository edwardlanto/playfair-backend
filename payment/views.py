import datetime
import bleach
from django.utils import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max, Count
from rest_framework.pagination import PageNumberPagination
from company.serializers import BaseCompanySerializer
from .models import Payment
from candidate.models import AppliedJob
from candidate.models import SavedJob
from candidate.serializers import AppliedJobSerializer
from django.shortcuts import get_object_or_404
from playfairauth.models import CustomUserModel
from company.models import Company
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import JsonResponse
from django.core import serializers
from django.db import transaction
from datetime import date
import stripe
import os
import asyncio

stripe.api_key = os.environ.get("STRIPE_TEST_API")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_company_bank_account(request):
    try:
        with transaction.atomic():  
            data = request.data
            instance = stripe.Token.create(
                bank_account={
                    "country": bleach.clean(data['country']),
                    "currency": bleach.clean(data['currency']),
                    "account_holder_name": bleach.clean(data['account_holder_name']),
                    "account_holder_type": "company",
                    "routing_number": bleach.clean(data['routing_number']),
                    "account_number": bleach.clean(data['account_number']),
                },
            )

            if(instance):
                company = Company.objects.filter(user=request.user).first()
                company.stripe_bank_token = instance.id
                company.save()

            return Response({"instance": instance}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_company_account(request):
    try:
        with transaction.atomic():
            data = request.data
            user = request.user
            company = Company.objects.get(user=user)
            instance = stripe.Account.create(
                country=company.country_code,
                type="custom",
                external_account = data['external_account'],
                business_type="company",
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                business_profile = {
                    "mcc": 7623,
                    "url": data['company_website'] if data['company_website'] != None else "https://playfairwork.com",
            },
                tos_acceptance = {
                    "date": data['created'],
                    "ip": data['ip']
            },
                company={
                    "name": bleach.clean(data['company_name']),
                    "phone": data['company_phone'],
                    "tax_id": data['tax_id'],
                    "address": {
                        "line1": bleach.clean(data['company_line1']),
                        "city": bleach.clean(data['company_city']),
                        "state": bleach.clean(data['company_state']),
                        "postal_code": bleach.clean(data['company_postal_code'])
                    },
                },
            )

            if(instance):
                company.stripe_account = bleach.clean(instance.stripe_id)
                company.save()

            return Response({"instance": instance}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_company_person(request):
    try:
        data = request.data
        user = request.user
        company = Company.objects.filter(user=user).first()
        address_array = data['line1'].split(',')
        address = address_array[0]
        state_info_array = address_array[2].strip().split(' ')
        city = address_array[1]
        state = state_info_array[0]
        postal_code = f"{state_info_array[1]} {state_info_array[2]}"
        date_array = data['dob'].split('-')
        instance = stripe.Account.create_person(
            company.stripe_account if company.stripe_account else data['account'], 
                first_name = bleach.clean(data['first_name']),
                last_name = bleach.clean(data['last_name']),
                email = bleach.clean(data['email']),
                phone = bleach.clean(data['phone']),
                id_number = bleach.clean(data['id_number']),
                dob = {
                    'day': int(date_array[2]),
                    'month': int(date_array[1]),
                    'year': int(date_array[0]),
                },
                address = {
                    'line1': address,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code,
                },
                relationship = {
                    'representative': data['representative'],
                    'percent_ownership': 100,
                    'owner': data['owner'],
                    'title': bleach.clean(data['title']),
                }
        )

        company = Company.objects.filter(user=request.user).first()
        company.stripe_person = instance.id
        company.save()

        return Response({"instance": instance}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
async def update_company_person(request):
    try:
        data = request.data
        user = request.user
        instance = await stripe.accounts.update_person(
            data['account'],
            data['person'], {
                'verification': {
                    'document': {
                        'front': data['front']
                    }
                }
            }
        )

        return Response({"instance": instance}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_front_company_file(request):
    try:
        user = request.user
        company = Company.objects.filter(user=user).first()
        upload = request.FILES['front']
        if 'front' not in request.FILES:
            return Response({"error": "Please upload your file"})
        with open(upload.file.name, "rb") as fp:
            front = stripe.File.create(
                purpose='identity_document',
                file=fp,
                stripe_account=company.stripe_account,
            )

            if(front.id):
                company = Company.objects.filter(user=user).first()
                company.stripe_id_front = front.id
                company.save()

        if 'back' not in request.FILES:
            print('No File in Back')
        else:
            with open(upload.file.name, "rb") as fp:
                back = stripe.File.create(
                    purpose='identity_document',
                    file=fp,
                    stripe_account=company.stripe_account,
                )
            if(back.id):
                company = Company.objects.filter(user=user).first()
                company.stripe_id_back = back.id
                company.save()
                
        return Response({"front": front, 'back': back}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def attach_company_file(request):
    try:
        data = request.data
        user = request.user
        company = Company.objects.filter(user=user).first()
        if company.stripe_id_back != None and company.stripe_id_front != None:
            obj = {
                'front': company.stripe_id_front,
                'back': company.stripe_id_back,
            }
        elif company.stripe_id_front != None and company.stripe_id_back == None:
            obj = {
                'front': company.stripe_id_front,
            }
        elif company.stripe_id_back != None and company.stripe_id_front == None:
            obj = {
                'back': company.stripe_id_back
            }

        instance = stripe.Account.modify(
            company.stripe_account,
            company={"verification": {"document": obj}},
        )

        return Response({"instance": instance}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)