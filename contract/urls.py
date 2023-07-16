from django.urls import path
from . import views

urlpatterns = [

    path('index', views.index, name='get-contracts'),
    path('verify/', views.verify, name='verify-contract'),
    path('create', views.create, name='create-contract'),
    path('<str:pk>/', views.get, name='confirm-contract'),
    path('confirm/<str:pk>', views.confirm_contract, name='confirm-contract'),
    path('update/<str:pk>', views.update, name='confirm-contract'),
    path('apply/<str:pk>', views.apply, name='apply'),
    path('managed', views.managed_contracts, name='managed_contracts'),
    path('managed/approve/<str:pk>/<str:user>', views.approve_contract, name='approve_contract'),
    path('managed/delete/<str:pk>/<str:user>', views.delete_contract, name='delete_contract'),
    path('pause/<str:pk>', views.pause_contract, name='pause_contract'),
    path('', views.confirm_contract, name='confirm-contract'),
]