from rest_framework import serializers
from .models import Company
from job.models import Job
from candidate.models import SavedCompany
from playfairauth.serializers import CustomUserSerializer
from playfairauth.models import CustomUserModel

class CompanySerializer(serializers.ModelSerializer):
    jobs_available = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    def get_is_saved(self, obj):
        saved = SavedCompany.objects.filter(company=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved
    
    def get_jobs_available(self, obj):
        return Job.objects.filter(company=obj.id, is_active=True).count()
    
    class Meta:
        model = Company
        fields = '__all__'

class ProfileCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class BaseCompanySerializer(serializers.ModelSerializer):
    jobs_available = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    def get_is_saved(self, obj):
        saved = SavedCompany.objects.filter(company=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved

    def get_jobs_available(self, obj):
        return Job.objects.filter(company=obj.id, is_active=True).count()
    
    class Meta:
        model = Company
        fields = ('name', 'logo', 'id', 'uuid', 'country_code',
        'country', 'city', 'state', 'industry', 'jobs_available', 'is_saved', 'website', 'address', 'postal_code')

class MinCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'id')