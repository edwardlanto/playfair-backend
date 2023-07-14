from django.urls import path
from . import views

urlpatterns = [
    path('', views.confirm_contract, name='confirm-contract'),
    path('index', views.index, name='get-contracts'),
    path('verify/', views.verify, name='verify-contract'),
    path('create', views.create, name='create-contract'),
    path('<str:pk>/', views.get, name='confirm-contract'),
    path('confirm/<str:pk>', views.confirm_contract, name='confirm-contract'),
    path('update/<str:pk>', views.update, name='confirm-contract'),
    # path('gig/create/milestone', views.createMilestoneGig, name='create_milestone_gig'),
    # path('gig/create/', views.create_gig, name='create_gig'),
]