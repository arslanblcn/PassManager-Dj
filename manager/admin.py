from django.contrib import admin
from .models import CreatePasswordModel
# Register your models here.

class PasswordAdmin(admin.ModelAdmin):
    list_display = ['id', 'password', 'created_date','retired_date', 'used_for_website']

admin.site.register(CreatePasswordModel, PasswordAdmin)