from rest_framework import serializers
from .models import Company
from job.models import Job
from candidate.models import SavedCompany
from playfairauth.serializers import CustomUserSerializer, ChatModelSerializer
from playfairauth.models import CustomUserModel

class CompanySerializer(serializers.ModelSerializer):
    jobs_available = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    user = ChatModelSerializer()

    def get_is_saved(self, obj):
        saved = SavedCompany.objects.filter(company=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved
    
    def get_jobs_available(self, obj):
        return Job.objects.filter(company=obj.id, is_active=True).count()
    
    class Meta:
        model = Company
        fields = ('id', 'jobs_available', 'is_saved', 'is_active', 'uuid', 'name', 'description', 'email', 'industry', 'phone', 'postal_code', 'address', 'country', 'country_code', 'city', 'state', 'founded_in', 'website', 'lat', 'long', 'size', 'job_count', 'facebook', 'twitter', 'linkedIn', 'instagram', 'rating', 'logo', 'created_date', 'is_complete', 'user')

class ProfileCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class BaseCompanySerializer(serializers.ModelSerializer):
    jobs_available = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    user = ChatModelSerializer()

    def get_is_saved(self, obj):
        saved = SavedCompany.objects.filter(company=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved

    def get_jobs_available(self, obj):
        return Job.objects.filter(company=obj.id, is_active=True).count()
    
    class Meta:
        model = Company
        fields = ('name', 'logo', 'id', 'uuid', 'country_code', 'description',
        'country', 'city', 'state', 'industry', 'jobs_available', 'is_saved', 'website', 'address', 'postal_code', 'user')

class MinCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'id')