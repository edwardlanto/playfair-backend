from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_companies, name='companies'),
    path('profile/jobs/create/', views.new_job, name='new_job'),
    path('read/me/', views.read_my_company, name='read_my_company'),
    path('update/me', views.update_my_company, name='update_my_company'),
    path('logo/update', views.upload_company_logo, name="upload_company_logo"),
    path('user/company/<str:pk>/save/', views.saveCompany, name='save_company'),
    path('user/company/<str:pk>/unsave/', views.unsaveCompany, name='unsave_company'),
    path('profile/jobs/', views.get_my_company_jobs, name='get_my_company/_jobs'),
    path('profile/jobs/<str:pk>/update', views.update_job, name='update_job'),
    path('profile/jobs/<str:pk>/delete', views.delete_job, name='delete_job'),
    path('profile/jobs/candidates/', views.getMyCompanyJobCandidates, name='get_my_job_and_candidates'),
    path('profile/jobs/candidates/<str:pk>/', views.get_my_candidate_application, name='get_my_candidate'),
    path('profile/company/candidates/', views.getMyCompanyCandidates, name='get_my_candidates'),
    path('<str:pk>/', views.get_company, name='get_company'),

]