from django.contrib import admin

from chat.models import Conversation, Message, ConversationMember

admin.site.register(Conversation)
admin.site.register(ConversationMember)
admin.site.register(Message)