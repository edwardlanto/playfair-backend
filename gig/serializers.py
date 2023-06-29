from rest_framework import serializers
from .models import Gig

class GigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = '__all__'

    company_logo = serializers.SerializerMethodField()

    def get_company_logo(self, obj):
        return 

    def create(self, validated_data):
        # Additional logic for creating a Gig
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Additional logic for updating a Gig
        return super().update(instance, validated_data)