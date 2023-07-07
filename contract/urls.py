from django.urls import path
from . import views

urlpatterns = [
    path('', views.confirm_contract, name='confirm-contract'),
    path('confirm/<str:pk>', views.confirm_contract, name='confirm-contract'),
    # path('gig/create/milestone', views.createMilestoneGig, name='create_milestone_gig'),
    # path('gig/create/', views.create_gig, name='create_gig'),
]