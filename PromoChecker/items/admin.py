from django.contrib import admin
from .models import AppUser, TrackedItem


admin.site.register(AppUser)
admin.site.register(TrackedItem)
