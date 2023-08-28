from rest_framework import serializers
from .models import Contract, Image
from playfairauth.models import CustomUserModel
from playfairauth.serializers import LogoUserSerializer, ChatModelSerializer
from company.serializers import MinCompanySerializer
from candidate.models import SavedContract, AppliedContract

class ContractSerializer(serializers.ModelSerializer):
    user = ChatModelSerializer()
    is_saved = serializers.SerializerMethodField()
    applied = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_is_saved(self, obj):
        saved = SavedContract.objects.filter(contract=obj.id, user=self.context['request'].user.id if self.context else None).exists()
        return saved
    
    def get_applied(self, obj):
        applied = AppliedContract.objects.filter(contract=obj.id, user=self.context['request'].user.id).exists()
        return applied
    
    def get_images(self, obj):
        array = []
        images = Image.objects.filter(contract=obj.id).all()

        for x in images:
            print(x.image.url)
            array.append({
                "name": x.image.name,
                "url": x.image.url
            })
        return array
    
    class Meta:
        model = Contract
        fields = '__all__'

class BaseContractSerializer(serializers.ModelSerializer):
    user = LogoUserSerializer()
    applied_count = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()

    def get_applied_count(self, obj):
         applied_count = AppliedContract.objects.filter(contract=obj.id).count()
         return applied_count
    
    def get_preview(self, obj):
        preview = Image.objects.filter(contract=obj.id).first()
    
        if preview != None:
            print(preview)
            preview = preview.image.url
        else:
            preview = None

        return preview
    
    class Meta:
        model = Contract
        fields = ('id', 'preview', 'title', 'status', 'amount', 'created_date', 'contractor', 'user', 'applied_count', 'country', 'city')