from django.urls import path
from . import views

urlpatterns = [
    path('gigs/', views.GigListView.as_view(), name='gig-list-create'),
    path('gigs/<int:pk>/', views.GigDetailView.as_view(), name='gig-detail'),
    path('gig/create/milestone', views.createMilestoneGig, name='create_milestone_gig'),
    path('gig/create/', views.create_gig, name='create_gig'),
]