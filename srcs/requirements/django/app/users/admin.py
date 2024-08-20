from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django.contrib import admin
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
  list_display = ('username', 'email', 'total_wins', 'total_losses', 'is_active', 'is_superuser', 'is_staff')
  
  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('email',)}),
    ('Game stats', {'fields': ('total_wins', 'total_losses')}),
    ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions', 'is_staff')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
  )
    
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('username', 'email', 'password1', 'password2', 'is_staff'),
    }),
  )
    
  search_fields = ('username', 'email')
  ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')