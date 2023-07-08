from datetime import timedelta
import django
from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel, CustomUserProfile
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserProfile
        exclude = ('user',)

class BaseUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserProfile
        fields = (
            "industry",
            "experience",
            "languages",
            "interests",
            "logo",
            "bio",
            "expected_salary",
            "created_date",
            "city",
            "title",
            "country",
            'first_name',
            'last_name',
            'id'
        )

class BaseUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = (
            "id",
            "username",
            "account_type",
            "first_name",
            "last_name"
        )

class ChatModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = (
            "username",
            "image"
        )


class FullUserProfileSerializer(serializers.ModelSerializer):
    is_complete = serializers.SerializerMethodField()

    def get_is_complete(self, obj):
        is_complete = CustomUserModel.objects.values_list('is_complete', flat=False).get(id=obj.user.id)[0]
        return is_complete

    class Meta:
        model = CustomUserProfile
        fields = '__all__'

class CustomUserSerializer(ModelSerializer):
    userprofile = BaseUserProfileSerializer()
    
    class Meta:
        model = CustomUserModel
        fields = [
            "id",
            "username",
            "userprofile",
            "account_type",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        user = CustomUserModel.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
            validated_data["account_type"],
            validated_data["first_name"],
        )

        return user
    
class FullCustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUserModel
        fields = [
            "id",
            "username",
            "account_type",
            "first_name",
            "last_name",
            "email"
        ]

    def create(self, validated_data):
        user = CustomUserModel.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
            validated_data["account_type"],
            validated_data["first_name"],
        )

        return user

    def create_company(self, validated_data):
        company = CustomUserModel.objects.create_company(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
            validated_data["account_type"],
            validated_data["first_name"],
        )

        return company
    
class SessionCustomUserSerializer(serializers.ModelSerializer):
    resume = serializers.SerializerMethodField()
    
    def get_resume(self, obj):
        resume = CustomUserProfile.objects.values_list('resume', flat=False).get(user=self.context['user'] )[0]
        
        return resume
    class Meta: 
        model = CustomUserModel
        fields = [
            "is_complete",
            "account_type",
            "resume"
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = authenticate(email=attrs["email"].lower(), password=attrs["password"])
        if user is not None:
            if user.is_active:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                access_token = refresh.access_token
                access_token.set_exp(lifetime=timedelta(days=10))
                try:
                    data['provider'] = 'credentials'
                    data['user'] = CustomUserSerializer(user).data
                    data["account_type"] = user.account_type
                    data["pf_refresh_token"]: str(refresh)
                    data['pf_access_token']: access_token
                    return data
                except Exception as e:
                    raise serializers.ValidationError("Something Wrong!")
            else:
                raise serializers.ValidationError("Account is Blocked")
        else:
            raise serializers.ValidationError(
                {"error": "Incorrect userid/email and password combination!"}
            )

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUserModel

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class LogoSerializer(serializers.Serializer):
    logo = serializers.CharField()
