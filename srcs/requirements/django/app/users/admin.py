from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models.Profile_model import Profile
from users.models.User_model import CustomUser
from users.models.FriendRequest_model import FriendRequest
from django.contrib import admin
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
  list_display = ('username', 'email', 'total_wins', 'total_losses', 'is_active', 'is_superuser', 'is_staff')
  
  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('email',)}),
    ('Game stats', {'fields': ('total_wins', 'total_losses')}),
    ('Friends & Blocked Users', {'fields': ('friends', 'blocked_users')}),
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
  filter_horizontal = ('friends', 'blocked_users', 'groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'image')
  
class FriendRequestAdmin(admin.ModelAdmin):
  model = FriendRequest
  list_display = ['from_user', 'to_user']
  search_fields = ['from_user__username', 'to_user__username']
  list_filter = ['from_user', 'to_user']

  actions = ['accept_friend_requests', 'reject_friend_requests']

  def accept_friend_requests(self, request, queryset):
    for friend_request in queryset:
      friend_request.to_user.friends.add(friend_request.from_user)
      friend_request.from_user.friends.add(friend_request.to_user)
      friend_request.delete()
    self.message_user(request, "Selected friend requests have been accepted.")

  accept_friend_requests.short_description = 'Accept selected friend requests'

  def reject_friend_requests(self, request, queryset):
      queryset.delete()
      self.message_user(request, "Selected friend requests have been rejected.")

  reject_friend_requests.short_description = 'Reject selected friend requests'

admin.site.register(FriendRequest, FriendRequestAdmin)
