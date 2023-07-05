from django.db import models
import uuid
from playfairauth.models import CustomUserModel

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=True)
    last_message = models.CharField(max_length=128, blank=True)
    last_message_user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, related_name="last_message_user", null=True)

    class Meta:
        db_table = "conversation"

class ConversationMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="conversation_member_id")
    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, related_name="conversation_member_user", null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    left_date = models.DateTimeField(auto_now_add=True)
    online = models.ManyToManyField(to=CustomUserModel, blank=True)

    class Meta:
        db_table = "conversation_member"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    from_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="from_user")
    content = models.CharField()
    created_date = models.DateTimeField(auto_now_add=True)
    # read = models.BooleanField(default=False)

    class Meta:
        db_table = "message"
