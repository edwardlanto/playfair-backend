from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests
import os
from rest_framework.response import Response
from rest_framework import status, generics
from gig.models import Gig
from gig.serializers import GigSerializer
from rest_framework import generics, pagination
import math
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_gig(request):
    print(os.environ.get('ESCROW_SANDBOX_API'))
    transaction = requests.post(
        'https://api.escrow-sandbox.com/integration/pay/2018-03-31',
        auth=('edwardlanto.developer+seller@gmail.com', os.environ.get('ESCROW_SANDBOX_API')),
        json={
            "currency": "usd",
            "description": "Perfect sedan for the snow2",
            "reference": "test-transact2",
            "return_url": "https://www.escrow-sandbox.com",
            "redirect_type": "manual",
            "items": [
                {
                    "extra_attributes": {
                        "make": "BMW",
                        "model": "328xi",
                        "year": "2008",
                    },
                    "fees": [
                        {
                            "payer_customer": "me",
                            "split": "1",
                            "type": "milestone",
                        },
                    ],
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": 8000,
                            "payer_customer": "hello.factauto@gmail.com",
                            "beneficiary_customer": "me",
                        },
                    ],
                    "title": "BMW 328xi",
                    "type": "milestone",
                },
            ],
            "parties": [
                {
                    "address": {
                        "line1": "180 Montgomery St",
                        "line2": "Suite 650",
                        "city": "San Francisco",
                        "state": "CA",
                        "country": "US",
                        "post_code": "94104",
                    },
                    "agreed": False,
                    "customer": "hello.factauto@gmail.com",
                    "date_of_birth": "1980-07-18",
                    "first_name": "John",
                    "initiator": False,
                    "last_name": "Wick",
                    "phone_number": "4155555555",
                    "lock_email": False,
                    "role": "buyer",
                },
                {
                    "agreed": False,
                    "customer": "me",
                    "initiator": True,
                    "role": "seller",
                },
            ],
        },
    )
    return Response({
        "company": transaction
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createMilestoneGig(request):

    transaction = requests.post(
        'https://api.escrow-sandbox.com/2017-09-01/transaction',
        auth=('edwardlanto.developer+seller@gmail.com', os.environ.get('ESCROW_SANDBOX_API')),
        json={
            "parties": [
                {
                    "role": "buyer",
                    "customer": "me"
                },
                {
                    "role": "seller",
                    "customer": "hello.factauto@gmail.com"
                }
            ],
            "currency": "usd",
            "description": "New Idea",
            "items": [
                {
                    "title": "Script 222",
                    "description": "Reading the script",
                    "type": "milestone",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": 10000.0,
                            "payer_customer": "me",
                            "beneficiary_customer": "hello.factauto@gmail.com"
                        }
                    ]
                },
                {
                    "title": "Story boards",
                    "description": "Doing the story22 boards",
                    "type": "milestone",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": 1000000.0,
                            "payer_customer": "me",
                            "beneficiary_customer": "hello.factauto@gmail.com"
                        }
                    ]
                },
                {
                    "title": "Acting 1",
                    "description": "Acting for car crash scene 1",
                    "type": "milestone",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": 200000.0,
                            "payer_customer": "me",
                            "beneficiary_customer": "hello.factauto@gmail.com"
                        }
                    ]
                },
                {
                    "title": "Acting 2",
                    "description": "Acting for helicopter jump scene 2",
                    "type": "milestone",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": 50000.0,
                            "payer_customer": "me",
                            "beneficiary_customer": "hello.factauto@gmail.com"
                        }
                    ]
                },
            ]
        },
    )

    return Response({
        "company": transaction
    }, status=status.HTTP_200_OK)

# @permission_classes([IsAuthenticated])
class GigListView(generics.ListAPIView):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer

class GigDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    pagination_class = pagination.PageNumberPagination()
