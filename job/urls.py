from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobs'),
    path('home/', views.homeJobs, name='home_jobs'),
    path('<str:pk>/', views.get_job, name='job'),
    path('<str:pk>/pause/', views.pauseJob, name='pause_job'),
    path('<str:pk>/start/', views.startJob, name='start_job'),
    # path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats'),
    # path('me/jobs/applied/', views.getCurrentUserAppliedJobs, name='current_user_applied_jobs'),
    # path('me/jobs/', views.getCurrentUserJobs, name='current_user_jobs'),
    # path('job/<str:pk>/candidates/', views.getCandidatesApplied, name='get_candidates_applied'),
    path('candidates/approve/<str:pk>/', views.approveCandidate, name='approve_job'),
    path('candidates/delete/<str:pk>/<str:ck>/', views.deleteCandidateApplication, name='delete_job')
]