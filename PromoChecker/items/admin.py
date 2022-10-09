from typing import Tuple
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser, TrackedItem


class AppUserAdmin(UserAdmin):
    list_display: Tuple = ('email', 'date_joined', 'is_admin', 'is_staff')
    search_fields: Tuple = ('email',)
    readonly_fields: Tuple = ('id', 'date_joined')
    ordering: Tuple = ('email',) 
    
    filter_horizontal: Tuple = ()
    list_filter: Tuple = ()
    fieldsets: Tuple = ()


admin.site.register(TrackedItem)
admin.site.register(AppUser, AppUserAdmin)
