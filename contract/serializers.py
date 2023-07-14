from rest_framework import serializers
from .models import Contract
from playfairauth.models import CustomUserModel
from playfairauth.serializers import LogoUserSerializer
from company.serializers import MinCompanySerializer
from candidate.models import SavedContract

class ContractSerializer(serializers.ModelSerializer):
    company = MinCompanySerializer()
    user = LogoUserSerializer()
    is_saved = serializers.SerializerMethodField()

    def get_is_saved(self, obj):
        saved = SavedContract.objects.filter(contract=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved
    
    class Meta:
        model = Contract
        fields = '__all__'

class BaseContractSerializer(serializers.ModelSerializer):
    company = MinCompanySerializer()
    user = LogoUserSerializer()

    # def get_logo(self, obj):
    #     user = CustomUserModel.objects.filter(id=obj.user.id).first()
    #     logo = user.image
    #     return logo
    
    class Meta:
        model = Contract
        fields = ('id', 'title', 'amount', 'created_date', 'user', 'company')