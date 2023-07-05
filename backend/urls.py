from django.contrib import admin
from django.urls import path, include, re_path
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/jobs/', include('job.urls')),
    path('api/companies/', include('company.urls')),
    path("api/accounts/", include("playfairauth.urls")),
    path("api/candidates/", include("candidate.urls")),
    path("api/payments/", include("payment.urls")),
    path('api/gigs', include('gig.urls')),

]
