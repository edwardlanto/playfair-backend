import bleach
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from company.models import Company
from chat.models import Conversation
from playfairauth.models import Contractor, CustomUserModel
from playfairauth.serializers import FullCustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from contract.models import Contract
import math
from candidate.models import AppliedContract
from playfairauth.models import CustomUserProfile
import stripe
import os
from candidate.models import AppliedContract
import bleach
from geopy.geocoders import Nominatim
import geocoder
import json
from django.contrib.auth.models import Group

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
def upload_verification_file(request):
    try:
        user = request.user
        stripe_account_id = None

        if user.groups.filter(name='contractor').exists():
            stripe_account_id = Contractor.objects.get(user=user.id).stripe_account

        if user.groups.filter(name='company').exists():
            stripe_account_id = Company.objects.get(user=user.id).stripe_account

        upload = request.FILES['front']
        if 'front' not in request.FILES:
            return Response({"error": "Please upload your file"})
        with open(upload.file.name, "rb") as fp:
            front = stripe.File.create(
                purpose='identity_document',
                file=fp,
                stripe_account=stripe_account_id,
            )

            if(front.id):
                if user.groups.filter(name='contractor').exists():
                    contractor = Contractor.objects.get(user=user.id)
                    contractor.stripe_id_front = front.id
                    contractor.save()

                if user.groups.filter(name='company').exists():
                    company = Company.objects.filter(user=user).first()
                    company.stripe_id_front = front.id
                    company.save()

        if 'back' not in request.FILES:
            return Response({"error": "Please upload your file"})
        else:
            with open(upload.file.name, "rb") as fp:
                back = stripe.File.create(
                    purpose='identity_document',
                    file=fp,
                    stripe_account=stripe_account_id,
                )
            if(back.id):
                if user.groups.filter(name='contractor').exists():
                    contractor = Contractor.objects.get(user=user.id)
                    contractor.stripe_id_back = back.id
                    contractor.save()

                if user.groups.filter(name='company').exists():
                    company = Company.objects.filter(user=user).first()
                    company.stripe_id_back = back.id
                    company.save()
        contractorGroup = Group.objects.get(name='contractor') 
        contractorGroup.user_set.add(user.id)
        return Response({"front": front.id, "back": back.id}, status=status.HTTP_200_OK)
        # return Response({"front": front, 'back': back}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": "Error with verification uploads."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_contractor_bank_account(request):
    try:
        with transaction.atomic():
            data = request.data
            user = request.user
            geolocator = Nominatim(user_agent="PlayfairGeoPy")
            location = geolocator.reverse(data['lat'] + "," + data['lng'])
            address = location.raw['address']
            dob_arr = data['formatted_dob'].split('-')
            f = open('data/stripe-currencies.json')
            curreny_json = json.load(f)
            currency_obj = [x for x in curreny_json['json_array'] if x['countryCode'].lower() == address['country_code'].lower()]
            profile = CustomUserProfile.objects.filter(user=request.user).first()
            profile.dob = data['formatted_dob']
            profile.country_code = address['country_code'].upper()
            profile.save()

            if len(currency_obj) == 0:
                currency = "CAD"
            else:
                currency = currency_obj[0]['currencyCode'].upper()

            bank_instance = stripe.Token.create(
                bank_account={
                    "country": bleach.clean(address['country_code']),
                    "currency": bleach.clean(currency),
                    "account_holder_name": bleach.clean(data['account_holder_name']),
                    "account_holder_type": "individual",
                    "routing_number": bleach.clean(data['routing_number']),
                    "account_number": bleach.clean(data['account_number']),
                },
            )

            contractor = Contractor.objects.filter(user=request.user).first()

            if(contractor == None):
                contractor = Contractor.objects.create(
                    user = request.user,
                    stripe_bank_token = bank_instance.id,
                    account_holder_name = bleach.clean(data['account_holder_name'])
                )
                contractor.save()

                account_instance = stripe.Account.create(
                    country=profile.country_code,
                    type="custom",
                    external_account = bank_instance.id,
                    business_type="individual",
                    capabilities={
                        "card_payments": {"requested": True},
                        "transfers": {"requested": True},
                    },
                    business_profile = {
                        "mcc": 7623,
                        "url": "",
                    },
                    tos_acceptance = {
                        "date": bank_instance.created,
                        "ip": bank_instance.client_ip
                },
                    individual={
                        "first_name": bleach.clean(user.first_name),
                        "last_name": bleach.clean(user.last_name),
                        "phone": data['phone'],
                        "id_number": data['id_number'],
                        "dob": {
                            'day': int(dob_arr[2]),
                            'month': int(dob_arr[1]),
                            'year': int(dob_arr[0]),
                        },
                        "address": {
                            "line1": bleach.clean(data['line1']),
                            "city": bleach.clean(address['city']),
                            "state": bleach.clean(address['state']),
                            "postal_code": bleach.clean(address['postcode'])
                        },
                    },
                )
                contractor.stripe_account = account_instance.id
                contractor.save()


            else:
                contractor.account_holder_name = bleach.clean(data['account_holder_name']),
                contractor.stripe_bank_token = bank_instance.id
                contractor.save()

                account_instance = stripe.Account.modify(
                    contractor.stripe_account,
                    external_account = bank_instance.id,
                    business_type="individual",
                    capabilities={
                        "card_payments": {"requested": True},
                        "transfers": {"requested": True},
                    },
                    business_profile = {
                        "mcc": 7623,
                        "url": "",
                    },
                    tos_acceptance = {
                        "date": bank_instance.created,
                        "ip": bank_instance.client_ip
                },
                    individual={
                        "first_name": bleach.clean(user.first_name),
                        "last_name": bleach.clean(user.last_name),
                        "phone": data['phone'],
                        "id_number": data['id_number'],
                        "dob": {
                            'day': int(dob_arr[2]),
                            'month': int(dob_arr[1]),
                            'year': int(dob_arr[0]),
                        },
                        "address": {
                            "line1": bleach.clean(data['line1']),
                            "city": bleach.clean(address['city']),
                            "state": bleach.clean(address['state']),
                            "postal_code": bleach.clean(address['postcode'])
                        },
                    },
                )

            # Create Person 
            # person_instance = stripe.Account.create_person(
            #     contractor.stripe_account, 
            #         first_name = bleach.clean(data['first_name']),
            #         last_name = bleach.clean(data['last_name']),
            #         email = bleach.clean(user.email),
            #         phone = bleach.clean(data['phone']),
            #         id_number = bleach.clean('4088675309'),
            #         dob = {
            #             'day': int(dob_arr[2]),
            #             'month': int(dob_arr[1]),
            #             'year': int(dob_arr[0]),
            #         },
            #         address = {
            #             'line1': data['line1'],
            #             'city': address['city'],
            #             'state': address['state'],
            #             'postal_code': address['postcode'],
            #         },
            #         relationship = {
            #             # 'representative': False,
            #             'percent_ownership': 100,
            #             'owner': True,
            #             'title': bleach.clean(data['title']),
            #         }
            # )


            return Response({"account_instance": account_instance}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def create_contractor_account(request):
#     try:
#         with transaction.atomic():
#             data = request.data
#             user = request.user
#             dob_arr = data['dob'].split('/')
#             geolocator = Nominatim(user_agent="PlayfairGeoPy")
#             location = geolocator.reverse(data['lat'] + "," + data['long'])
#             address = location.raw['address']
#             profile = CustomUserProfile.objects.filter(user=request.user).first()
#             contractor = Contractor.objects.filter(user=user).first()
#             instance = stripe.Account.create(
#                 country=profile.country_code,
#                 type="custom",
#                 external_account = data['external_account'],
#                 business_type="individual",
#                 capabilities={
#                     "card_payments": {"requested": True},
#                     "transfers": {"requested": True},
#                 },
#                 business_profile = {
#                     "mcc": 7623,
#                     "url": "",
#                 },
#                 tos_acceptance = {
#                     "date": data['created'],
#                     "ip": data['ip']
#             },
#                 individual={
#                     "first_name": bleach.clean(user.first_name),
#                     "last_name": bleach.clean(user.last_name),
#                     "phone": data['phone'],
#                     "id_number": data['id_number'],
#                     "dob": {
#                         'day': int(dob_arr[2]),
#                         'month': int(dob_arr[1]),
#                         'year': int(dob_arr[0]),
#                     },
#                     "address": {
#                         "line1": bleach.clean(data['line1']),
#                         "city": bleach.clean(address['city']),
#                         "state": bleach.clean(address['state']),
#                         "postal_code": bleach.clean(address['postcode'])
#                     },
#                 },
#             )

#             if(instance):
#                 contractor.stripe_account = instance.id
#                 contractor.save()
#                 contractorGroup = Group.objects.get(name='contractor') 
#                 contractorGroup.user_set.add(user.id)
#                 return Response({"instance": instance, "message": "Person created"}, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(str(e))
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def account(request):
    user = CustomUserModel.objects.values('first_name', 'last_name').filter(id=request.user.id).first()
    groups = []
        
    for g in request.user.groups.all():
        groups.append(g.name)

    if request.user.groups.filter(name='contractor').exists():
        account_instance = Contractor.objects.filter(user=request.user).first()
        if account_instance != None:
            account_instance = stripe.Account.retrieve(account_instance.stripe_account)

        
        created = Contractor.objects.values().filter(user=request.user).first()
        if(created):
            created = True
        return Response({
            'account_created': True, 
            'user' : user, 
            'account_instance': account_instance,
            'groups': groups
        },status=status.HTTP_200_OK)

    return Response({
        'user' : user, 
        'groups': groups
    },status=status.HTTP_200_OK)
    
@api_view(['POST'])
def address(request):
    data = request.data
    # geolocator = Nominatim(user_agent="PlayfairGeoPy")
    # location = geolocator.reverse(data['lat'] + "," + data['long'])
    # address = location.raw['address']
    # print(address)

    # g = geocoder.canadapost('7231 Sherbrooke St, Vancouver, BC V5X 4E3, Canada', key="887e5a7cb633632e:f524cc3fd1d9300fea322f")
    # print(g.postal)
    return Response()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_intent(request, pk):
    if request.method == 'POST':
        application = None
        return Response({'application': application}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        try:
            receipt = {}
            application = AppliedContract.objects.get(id=bleach.clean(pk))
            contract_title = Contract.objects.get(id=application.contract.id).title
            sub_total = application.amount * 100
            service_fee = int(application.amount) * 0.15 + 0.30
            service_fee = math.trunc(service_fee * 100)
            currency = Contract.objects.get(id=application.contract.id).currency
            total = sub_total + service_fee
            receipt['total'] = total
            receipt['sub_total'] = sub_total
            receipt['service_fee'] = service_fee
            if application.payment_intent == None:
                instance = stripe.PaymentIntent.create(
                    amount=total,
                    description=contract_title,
                    currency=currency['code'],
                    automatic_payment_methods={"enabled": True},
                )

                application.payment_intent = instance.id
                application.save()

                return Response({
                    'payment_intent': instance,
                    'receipt': receipt,
                }, status=status.HTTP_200_OK)
            else:
                instance = stripe.PaymentIntent.retrieve(
                    application.payment_intent,
                )
                return Response({
                    'payment_intent': instance,
                    'receipt': receipt,
                }, status=status.HTTP_200_OK)
                
        except AppliedContract.DoesNotExist:
            return Response({"error": "Could not find Application"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def payout_contractor(request, pk):
    try:
        if request.method == 'POST':
            try:
                application = AppliedContract.objects.get(id=pk)

                if application.status == 'Completed':
                    return Response({'error': 'Already paid out contractor.'},status=status.HTTP_400_BAD_REQUEST)
                
                contract = Contract.objects.get(id=application.contract.id)
                contractor = Contractor.objects.get(id=application.contractor.id)
                amount = round(float(application.amount)) * 100
                platform_fee = round(float(amount * 0.185))
                payout_amount = amount - platform_fee
                instance = stripe.Transfer.create(
                    amount=payout_amount,
                    currency=contract.currency['code'],
                    destination=contractor.stripe_account,
                )
                application.status = 'Completed'
                application.is_active = False
                application.save()

                return Response({'message': 'Successfully paid out', 'instance': instance},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if request.method == 'GET':
            application = AppliedContract.objects.values('id', 'contractor', 'amount', 'paid').filter(id=pk).first()

            if application['paid'] == False:
                return Response({'error': 'Contract not paid'},status=status.HTTP_400_BAD_REQUEST)
            
            contractor = Contractor.objects.get(id=application['contractor'])
            amount = application['amount'] * 0.029
            platform_fee = application['amount'] * 0.15

            return Response({'message': 'Successfully paid out', 'application': application, 'platform_fee': platform_fee},status=status.HTTP_200_OK)
    except AppliedContract.DoesNotExist:
        return Response({"error": "Could not find Application"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def payment_paid(request, pk):
    try:
        applied_contract = AppliedContract.objects.get(id=pk)
        applied_contract.paid = True
        applied_contract.status = 'In Progress'
        applied_contract.save()
        thread = Conversation.objects.get(application=applied_contract.id)
        return Response({'thread': thread.id})
    except Exception as e:
        return Response({'error': str(e)},status=status.HTTP_200_OK)



