from rest_framework import serializers
from .models import Message, Conversation
from playfairauth.models import CustomUserModel
from playfairauth.serializers import ChatModelSerializer

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return ChatModelSerializer(CustomUserModel.objects.get(id=obj.from_user.id)).data
    
    class Meta:
        model = Message
        exclude = ('conversation_id',)
class ConversationSerializer(serializers.ModelSerializer):


    class Meta: 
        model = Conversation
        fields = '__all__'
