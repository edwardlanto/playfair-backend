from django.urls import path
from . import views

urlpatterns = [
    path('create-company-bank-account/', views.create_company_bank_account, name='create_company_bank_account'),
    path('create-company-account/', views.create_company_account, name='create_company_account'),
    path('create-company-person/', views.create_company_person, name='create_company_person'),
    path('update-company-person/', views.update_company_person, name='update_company_person'),
    path('upload-company-file/', views.upload_front_company_file, name='upload_front_company_file'),
    path('attach-company-file/', views.attach_company_file, name='attach_company_file'),

    path('create-contractor-bank-account', views.create_contractor_bank_account, name='create_contractor_bank_account'),
    path('create-contractor-account', views.create_contractor_account, name='create_contractor_account'),
    path('verify-account', views.verify_account, name='verify_account'),
    path('address', views.address, name='address'),
    # path('contracts/<str:pk>', views.contract_info, name='contract-info'),
    path('payment-intent/<str:pk>', views.payment_intent, name='payment_intent'),
    # path('update-contractor-person/', views.update_contractor_person, name='update_contractor_person'),
    # path('upload-contractor-file/', views.upload_front_contractor_file, name='upload_front_contractor_file'),
    # path('attach-contractor-file/', views.attach_contractor_file, name='attach_contractor_file'),
]