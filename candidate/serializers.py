from django.http import JsonResponse
from rest_framework import serializers
from playfairauth.serializers import LogoUserSerializer
from job.serializers import JobSerializer, BaseJobSerializer
from playfairauth.models import CustomUserProfile
from chat.models import Conversation
from playfairauth.serializers import CustomUserSerializer, BaseUserProfileSerializer
from .models import SavedJob
from candidate.models import AppliedJob, AppliedContract
from company.models import Company
from company.serializers import BaseCompanySerializer
from playfairauth.models import CustomUserModel, Contractor
from job.models import Job

class AppliedJobSerializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    company = BaseCompanySerializer()
    job = BaseJobSerializer()

    def get_company(self, obj):
        return Company.objects.get(id=obj.company)

    def get_userprofile(self, obj):
        return BaseUserProfileSerializer(CustomUserProfile.objects.filter(user=obj.user).first()).data
    
    def get_last_name(self, obj):
        return CustomUserModel.objects.filter(id=obj.user.id).values_list('last_name', flat=True)[0]
    
    def get_first_name(self, obj):
        return CustomUserModel.objects.filter(id=obj.user.id).values_list('first_name', flat=True)[0]
    
    class Meta:
        model = AppliedJob
        fields = '__all__'

class BaseAppliedJobSerializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_userprofile(self, obj):
        return BaseUserProfileSerializer(CustomUserProfile.objects.filter(user=obj.user).first()).data
    
    def get_last_name(self, obj):
        return CustomUserModel.objects.filter(id=obj.user.id).values_list('last_name', flat=True)[0]
    
    def get_first_name(self, obj):
        return CustomUserModel.objects.filter(id=obj.user.id).values_list('first_name', flat=True)[0]
    
    class Meta:
        model = AppliedJob
        exclude = ('resume', 'coverLetter', 'job',)

class BaseContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = "__all__"

class BaseAppliedContractSerializer(serializers.ModelSerializer):
    user = LogoUserSerializer()
    profile = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return CustomUserProfile.objects.filter(user=obj.contractor.user).values('title', 'experience')
    
    def get_conversation(self, obj):
        return Conversation.objects.filter(contract=obj.contract).values('id').first()

    class Meta:
        model = AppliedContract
        fields = "__all__"

class AppliedContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedContract
        fields = "__all__"

class CandidateSavedJobSerializer(serializers.ModelSerializer):
    job = BaseJobSerializer()
    class Meta:
        model = SavedJob
        fields = '__all__'




