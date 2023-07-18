from django.contrib import admin
from .models import CustomUserModel, CustomUserProfile
from django.contrib.auth.admin import UserAdmin

class UserAdminWithGroup(UserAdmin):
    def group_name(self, obj):
        queryset = obj.groups.values_list('name',flat=True)
        groups = []
        for group in queryset:
            groups.append(group)
        
        return ' '.join(groups)

    list_display = UserAdmin.list_display + ('group_name',)

# admin.site.unregister(CustomUserModel)
admin.site.register(CustomUserModel, UserAdminWithGroup)
admin.site.register(CustomUserProfile)

