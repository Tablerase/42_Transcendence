from django.contrib import admin

# Register your models here.
from .models import Test_User

class TestUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'alive', 'spectator')

admin.site.register(Test_User, TestUserAdmin)