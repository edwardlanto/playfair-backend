from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from django.db import transaction
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from .serializers import *
from django.core import serializers
from company.serializers import BaseCompanySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from datetime import timedelta
from rest_framework.decorators import permission_classes, api_view
from company.models import Company
from rest_framework_simplejwt.views import TokenObtainPairView
from .oauth_serializers import *
from django.contrib.auth.models import Group
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from company.serializers import ProfileCompanySerializer
from xmlrpc.client import ResponseError
from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid
from django.utils import timezone
import os
import random
from geopy.geocoders import Nominatim
import requests

@permission_classes((AllowAny, ))
class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
    
@permission_classes((AllowAny, ))
class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

class CandidateView(generics.ListCreateAPIView):

    def post(self, request, *args, **kwargs):  
        try:
            user = {
                'username': request.data['email'], 
                'email': request.data['email'],
                'password': request.data['password'],
                'account_type': request.data['account_type'],
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name']
            }
                    
            queryset = CustomUserModel.objects.create_user(**user)
            serializer_class = CustomUserSerializer(queryset, many=False)

            return Response({ "user": serializer_class.data })
        except Exception as e:
            return Response({ "error": str(e) })
        
class EmployerView(generics.ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        try:
            # geolocator = Nominatim(user_agent="PlayFair")
            # location = geolocator.geocode(f"{request.data['country']['label']},{request.data['city']['label']}")
            with transaction.atomic():
                if CustomUserModel.objects.filter(email=request.data['email']).exists():
                    return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
                if Company.objects.filter(email=request.data['name']).exists():
                    return Response({"error": "Company name already in use."}, status=status.HTTP_400_BAD_REQUEST)                
                if request.data['account_type'] == 'company':
                    user = {
                        'email': request.data['email'].lower(),
                        'username': request.data['name'], 
                        'password': request.data['password'],
                        'account_type': request.data['account_type'],
                    } 
                    queryset = CustomUserModel.objects.create_user(**user)

                    if queryset.id != None:
                        company = Company.objects.create(
                            user=queryset,
                            name=request.data['name'],  
                            email = request.data['email'],
                            phone =  request.data['phone'],
                            industry = request.data['industry'],
                        )
                        company.save()
                        companyGroup = Group.objects.get(name='company') 
                        companyGroup.user_set.add(queryset.id)
                    serializer = CustomUserSerializer(queryset, many=False)
                    return Response({ "company": serializer.data })
                
                return Response({ "error": "Not implemented yet" })
        except Exception as e:
            return Response({ "error": str(e) })
        
class LoginView(TokenObtainPairView):
	"""
	Login View with jWt token authentication
	"""
	serializer_class = MyTokenObtainPairSerializer
        
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUserModel
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error": ["Password wasn't correct."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_is_candidate(request):
    isCandidate = request.user.groups.filter(name='candidate').exists()
        
    if isCandidate == True:
        return Response({"isCandidate": True}, status=status.HTTP_200_OK)
        
    return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
def get_is_employer(request):
    isEmployer = request.user.groups.filter(name='employer').exists()
        
    if isEmployer == True:
        return Response({"isEmployer": True}, status=status.HTTP_200_OK)
        
    return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def refresh_token(request):
    return Response({
        'refresh_token'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def me(request):
    try:
        user = request.user
        if user.groups.filter(name='company'):
            company = Company.objects.filter(user=request.user.id).first()
            user = CustomUserModel.objects.filter(id=company.user.id).first()
            return Response({
                'profile': ProfileCompanySerializer(company).data,
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        if user.groups.filter(name='candidate'):
            user = CustomUserModel.objects.filter(id=request.user.id).first()
            profile = CustomUserProfile.objects.filter(user=user).first()
            return Response({
                'profile': FullUserProfileSerializer(profile).data,
                'user': FullCustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)
    
    except Exception as e:
        
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def get_logo(request):
    user = request.user
    if(user.groups.filter(name='company').exists()):
        user = CustomUserModel.objects.filter(email=user.email).first()
        return Response({'logo': user.image.url}, status=status.HTTP_200_OK)
            
    if(user.groups.filter(name='candidate').exists()):
        userprofile = CustomUserProfile.objects.filter(user=request.user).first()
        if not userprofile.logo:
            return Response({'logo': None}, status=status.HTTP_200_OK)
        else:
            return Response({'logo': userprofile.logo.url}, status=status.HTTP_200_OK)
        
@api_view(["GET"])
def get_me(request):
    try:
        user = CustomUserModel.objects.get(email=request.user)

        if user == None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'user': ChatModelSerializer(user).data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def resume(request):
    try:
        profile = CustomUserProfile.objects.filter(user=request.user).values('resume', ).first()
        if profile:
            return Response({'profile': profile }, status=status.HTTP_200_OK)
        else:
            return Response({'profile': None }, status=status.HTTP_200_OK)
    except Exception as e:
            return Response({'error': str(e) }, status=status.HTTP_200_OK)

@transaction.atomic
@api_view(["POST"])
def register_candidate_credentials(request):
    try:
        user = {
            'username': request.data['email'], 
            'email': request.data['email'].lower(), 
            'password': request.data['password'], 
            'account_type': request.data['account_type'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name']
        }

        if CustomUserModel.objects.filter(email=request.data['email']).exists():
            return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUserModel.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = "credentials"
        user.save()
        if user.id != None and request.data["account_type"] == "candidate":
            profile = CustomUserProfile.objects.create(
                user_id = user.id,
                is_candidate = True,
                first_name = request.data["first_name"],
                last_name = request.data["last_name"],
            )
            profile.save()
            candidate = Group.objects.get(name='candidate') 
            candidate.user_set.add(user.id)
    
        return Response({
            'messaage': 'Succcessfully created user.'
            # 'provider': 'credentials',
            # 'user': SessionCustomUserSerializer(user,context={'user': new_user}).data,
            # 'account_type': new_user.account_type,
            # 'tokens': str(new_token[0]['key']),
            # 'pf_refresh_token': str(refresh),
            # 'pf_access_token': access_token,
        }, status=status.HTTP_200_OK)

    except Exception as e:
            return Response({'error': str(e) }, status=status.HTTP_200_OK)        
    
@api_view(['GET'])
def getCsrf(request):
    django.middleware.csrf.get_token(request)
    return Response({'token': 'token'})

@api_view(['POST'])
def forgot_password(request):
    token = uuid.uuid1(random.randint(0, 281474976710655))
    user = CustomUserModel.objects.filter(email=request.data['email']).first()
    if(user == None):
        return Response(status=status.HTTP_204_NO_CONTENT)
    userId = user.id
    email = request.data['email']
    user.forgot_password_token = token
    user.forgot_password_timestamp = timezone.now()
    user.save()
    subject = 'Forgot Password Reset'
    domain = 'playfairwork.com'
    c = {
        "email": email,
        'domain': domain,
        'site_name': 'PlayFair',
        'token': token,
        'url': '{}/forgot-password-reset'.format(os.environ.get('FRONTEND_URL')),
        'userId': userId
    }

    if user.auth_provider == 'credentials':
        msg_html = render_to_string('forgot_password.html', c)
        send_mail(subject, '', 'playfair.work@gmail.com', [email], html_message=msg_html)

    return Response({'message': 'A password reset has been sent to your account if found.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_password_reset(request):
    user = CustomUserModel.objects.filter(forgot_password_token=request.GET.get('token')).first()
    created_time = user.forgot_password_timestamp
    current_time = timezone.now()
    total_difference = current_time - created_time
    total_difference = int(total_difference.total_seconds() / 60)
    if total_difference > 110:
        return Response({'result': 'expired'}, status=status.HTTP_423_LOCKED)
    
    return Response({'message': 'Successfully Changed Password',
                     'result': True}, status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset_done(request):
    user = CustomUserModel.objects.filter(forgot_password_token=request.data['token']).first()
    print(user)
    if user == None:
        return Response({'error': 'Could not find user'}, status=status.HTTP_200_OK)           
    
    user.set_password(request.data['new_password'])
    user.forgot_password_token = None
    user.forgot_password_timestamp = None
    user.save()

    return Response({'message': 'Successfully Changed Password'}, status=status.HTTP_200_OK)              

@api_view(['POST'])
def subscribe(request):
    subject = 'Email Subscription',
    c = {
        "email": request.data['email']
    }

    msg_html = render_to_string('subscribe_email.html', c)
    send_mail(subject, '', 'noreply@playfairwork.com', ['playfair.work@gmail.com'], html_message=msg_html)

    return Response({'message': 'You have successfully subscribed to PlayFair.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_is_complete(request):
    user = request.user
    is_complete = CustomUserModel.objects.filter(user=user).first().is_complete

    return Response({'is_complete': is_complete}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_geo_location(request):
    return Response({'geo_location': get_location(request)})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(request):
    ip_address = get_client_ip(request)
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data