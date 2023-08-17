from library.sociallib import google
from library.sociallib import facebook
from library.register.register import register_social_user
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    account_type = serializers.CharField()
    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        
        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, account_type=self.initial_data['account_type'])
    
class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
        except:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )
        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)