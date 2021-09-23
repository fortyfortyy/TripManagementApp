from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    readonly_fields = ('id', 'date_joined', 'last_login')
