from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'company_name', 'created_at')
    list_filter = ('company_name',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'company_name')
    ordering = ('last_name',)