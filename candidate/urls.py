from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_candidates, name='get_candidates'),
    path('jobs/<str:pk>/save/', views.save_job, name='save_job'),
    path('jobs/<str:pk>/apply/', views.apply_to_job, name='apply_to_job'),
    path('companies/create/', views.upgrade_to_company, name='update_to_company'),
    path('companies/create/logo/', views.upgrade_to_company_logo, name='update_to_company_logo'),
    path('companies/<str:pk>/save/', views.save_company, name='save_company'),
    path('companies/<str:pk>/unsave/', views.unsave_company, name='unsave_company'),
    path('jobs/<str:pk>/unsave/', views.unsave_job, name='unsave_job'),
    path('jobs/<str:pk>/check/', views.is_applied, name='is_applied_to_job'),
    path('upload/resume/', views.upload_candidate_resume,name='upload_candidate_resume'),
    path('upload/logo/', views.upload_candidate_logo,name='uploadCandidateLogo'),
    path('message-company/', views.candidate_message_company, name='candidate_message_company'),
    path('message-to-candidate/', views.message_to_candidate, name='message_to_candidate'),
    path('profile/jobs/applied-jobs/', views.getAppliedJobs, name='get_applied_jobs'),
    path('profile/jobs/applied-jobs/<str:pk>/',views.get_applied_job, name='get_applied_job'),
    path('profile/jobs/saved-jobs/', views.get_saved_jobs, name='get_saved_jobs'),
    path('profile/jobs/saved-jobs/<str:pk>/', views.delete_saved_job, name='delete_saved_job'),
    path('profile/resume/delete/', views.delete_resume, name='delete_resume'),
    path('profile/me/update/', views.update_me, name='update_user'),
    path('profile/update/', views.update_candidate_me, name='update_user'),
    path('logo/delete/', views.delete_logo, name='delete_logo'),
    path('<str:pk>/', views.get_candidate, name='get_candidate'),
    # path('logo/update/', views.upload_company_logo, name="upload_company_logo"),
]