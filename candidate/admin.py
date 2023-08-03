from django.contrib import admin
from .models import *

admin.site.register(Candidate)
admin.site.register(AppliedContract)
admin.site.register(AppliedJob)
admin.site.register(SavedJob)
admin.site.register(Contractor)

