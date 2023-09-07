from rest_framework import serializers
from .models import Job 
from candidate.models import AppliedJob
from candidate.models import SavedJob
from company.models import Company
from playfairauth.serializers import UserProfileSerializer, CustomUserSerializer, ChatModelSerializer
from company.serializers import CompanySerializer, BaseCompanySerializer

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    is_saved = serializers.SerializerMethodField()
    user = ChatModelSerializer()
    def get_is_saved(self, obj):
        saved = SavedJob.objects.filter(job=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved

    class Meta: 
        model = Job
        fields = '__all__'

class BaseJobSerializer(serializers.ModelSerializer):
    company = BaseCompanySerializer()
    is_saved = serializers.SerializerMethodField()
    candidates = serializers.SerializerMethodField()
    user = ChatModelSerializer()

    def get_is_saved(self, obj):
        saved = SavedJob.objects.filter(job=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved
    
    def get_candidates(self, obj):
        return AppliedJob.objects.filter(job=obj.id).count()

    class Meta: 
        model = Job
        fields = ('id', 'uuid', 'title', 'min_salary', 'max_salary', 'created_date', 'company', 'type', 'is_saved', 'city', 'country', 
                  'candidates', 'is_remote', 'is_commission', 'is_active', 'work_status', 'rate_type', 'user', 'skills', 'description')

