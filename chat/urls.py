from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>', views.get_conversation, name='conversation'),
]