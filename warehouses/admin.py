# warehouses/admin.py
from django.contrib import admin
# Barcha modellar import qilinganiga ishonch hosil qiling
from .models import Warehouse, Inventory, StockIn, StockOut

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity_sqm', 'contact_person', 'is_active', 'created_at')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'location', 'contact_person', 'phone_number')
    date_hierarchy = 'created_at' # Sana bo'yicha navigatsiya
    ordering = ('name',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'last_updated')
    list_filter = ('warehouse', 'product') # Ombor va mahsulot bo'yicha filter
    search_fields = ('product__name', 'warehouse__name') # Mahsulot va ombor nomlari bo'yicha qidirish
    raw_id_fields = ('product', 'warehouse') # Agar mahsulotlar va omborlar ko'p bo'lsa qulay
    ordering = ('warehouse__name', 'product__name') # Saralash

# Yangi qo'shilgan modellar uchun admin sozlamalari:
@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'product', 'quantity', 'in_date', 'reason')
    list_filter = ('warehouse', 'product', 'in_date')
    search_fields = ('warehouse__name', 'product__name', 'reason')
    readonly_fields = ('in_date',) # Sana avtomatik to'ldiriladi, tahrirlashga ruxsat bermaslik
    raw_id_fields = ('warehouse', 'product') # Agar ro'yxatlar uzun bo'lsa qulay

@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'product', 'quantity', 'out_date', 'reason')
    list_filter = ('warehouse', 'product', 'out_date')
    search_fields = ('warehouse__name', 'product__name', 'reason')
    readonly_fields = ('out_date',) # Sana avtomatik to'ldiriladi, tahrirlashga ruxsat bermaslik
    raw_id_fields = ('warehouse', 'product') # Agar ro'yxatlar uzun bo'lsa qulay