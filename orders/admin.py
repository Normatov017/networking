from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'id')
    inlines = [OrderItemInline]
    date_hierarchy = 'order_date'
    raw_id_fields = ('customer',) # Katta ma'lumotlar uchun foydali

    # calculate total_amount on save
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.total_amount = sum(item.price * item.quantity for item in obj.items.all())
        obj.save() # Again save to update total_amount