import os
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from playfairauth.models import CustomUserModel, CustomUserProfile
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from playfairauth.serializers import SessionCustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import timedelta

@transaction.atomic
def register_social_user(provider, user_id, email, name, account_type):
    filtered_user_by_email = CustomUserModel.objects.filter(email=email)
    name_arr = name.split(" ")
    first_name = name_arr[0]
    last_name = name_arr[1]
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            new_user = CustomUserModel.objects.get(email=email)

            registered_user = CustomUserModel.objects.get(email=email)
            registered_user.check_password(os.environ.get('GOOGLE_API_SECRET'))

            Token.objects.filter(user=registered_user).delete()
            Token.objects.create(user=registered_user)
            new_token = list(Token.objects.filter(
            user_id=registered_user).values("key"))
            candidate = Group.objects.get(name='candidate') 
            candidate.user_set.add(registered_user.id)

            # Simple JWT Tokens #
            refresh = RefreshToken.for_user(registered_user) 

            return {
                'provider': 'google',
                'user': SessionCustomUserSerializer(new_user, context={'user': new_user}).data,
                'account_type': registered_user.account_type,
                'tokens': str(new_token[0]['key']),
                'pf_refresh_token': str(refresh),
                'pf_access_token': str(refresh.access_token),
            }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        print("USER RAN")
        user = {
            'username': email, 
            'email': email,
            'password': os.environ.get('GOOGLE_API_SECRET'),
            'account_type': account_type,
            'first_name': first_name,
            'last_name': last_name
        }
        user = CustomUserModel.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()
        if user.id != None and account_type == 'candidate':
            profile = CustomUserProfile.objects.create(
                user_id = user.id,
                is_candidate = True,
                first_name = first_name,
                last_name = last_name,
            )
            profile.save()
        new_user = CustomUserModel.objects.get(email=email)
        new_user.check_password(os.environ.get('GOOGLE_API_SECRET'))
        Token.objects.create(user=new_user)
        new_token = list(Token.objects.filter(user_id=new_user).values("key"))
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(days=10))
        
        return {
            'provider': 'google',
            'user': SessionCustomUserSerializer(new_user, context={'user': new_user}).data,
            'account_type': new_user.account_type,
            'tokens': str(new_token[0]['key']),
            'pf_refresh_token': str(refresh),
            'pf_access_token': str(refresh.access_token),
        }




