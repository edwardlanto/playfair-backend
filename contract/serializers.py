from rest_framework import serializers
from .models import Contract
from playfairauth.models import CustomUserModel
from playfairauth.serializers import LogoUserSerializer, ChatModelSerializer
from company.serializers import MinCompanySerializer
from candidate.models import SavedContract, AppliedContract

class ContractSerializer(serializers.ModelSerializer):
    user = ChatModelSerializer()
    is_saved = serializers.SerializerMethodField()
    applied = serializers.SerializerMethodField()

    def get_is_saved(self, obj):
        saved = SavedContract.objects.filter(contract=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved
    
    def get_applied(self, obj):
        applied = AppliedContract.objects.filter(contract=obj.id, user=self.context['request'].user.id).exists()
        return applied
    
    class Meta:
        model = Contract
        fields = '__all__'

class BaseContractSerializer(serializers.ModelSerializer):
    user = LogoUserSerializer()
    applied_count = serializers.SerializerMethodField()

    def get_applied_count(self, obj):
         applied_count = AppliedContract.objects.filter(contract=obj.id).count()
         return applied_count
    
    class Meta:
        model = Contract
        fields = ('id', 'title', 'status', 'amount', 'created_date', 'contractor', 'user', 'image', 'applied_count', 'country', 'city')