from django.urls import path
from . import views

urlpatterns = [
    path('create-company-bank-account/', views.create_company_bank_account, name='create_company_bank_account'),
    path('create-company-account/', views.create_company_account, name='create_company_account'),
    path('create-company-person/', views.create_company_person, name='create_company_person'),
    path('update-company-person/', views.update_company_person, name='update_company_person'),
    path('upload-company-file/', views.upload_front_company_file, name='upload_front_company_file'),
    path('attach-company-file/', views.attach_company_file, name='attach_company_file'),
]