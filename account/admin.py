from django.contrib import admin
from .models import User_Profile
# Register your models here.

class show_profiles(admin.ModelAdmin):
    list_display = ['user', 'telefon', 'geburtsdatum', 'Stadt']
admin.site.register(User_Profile, show_profiles)