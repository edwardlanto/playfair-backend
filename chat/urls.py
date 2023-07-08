from django.urls import path
from . import views

urlpatterns = [
    path('create-message', views.create_message, name='create-message'),   
    path('<str:pk>', views.get_conversation, name='conversation'),   

]