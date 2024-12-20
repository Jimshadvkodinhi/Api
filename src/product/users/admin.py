from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')  # Fields to display in the admin list view
    search_fields = ('user__username', 'name', 'phone')  # Fields to search within the admin panel
    list_filter = ('user', 'phone')  # Add filters for better navigation in the admin
    ordering = ('user',)  # Default ordering

admin.site.register(UserProfile, UserProfileAdmin)
