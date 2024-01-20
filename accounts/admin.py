from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email','username','first_name','last_name','is_active','is_staff','is_admin','role','date_joined','last_login')
    list_display_links = ('email','username','first_name','last_name')
    search_fields = ('email','username','first_name','last_name')
    readonly_fields = ('date_joined','last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','image_tag','image_tag2') 
    list_display_links = ('user','image_tag','image_tag2')

# Register your models here.
admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile,UserProfileAdmin)