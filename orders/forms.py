# orders/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from customers.models import Customer
from products.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    # Mijoz tanlashda faqat mavjud mijozlarni ko'rsatish va sortirovka qilish
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by('last_name', 'first_name'),
        empty_label="--- Mijozni tanlang ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select product-select'}), # JS uchun class
            'quantity': forms.NumberInput(attrs={'class': 'form-control item-quantity', 'min': '1'}), # JS uchun class
        }
    
    # Mahsulot tanlashda faqat faol mahsulotlarni ko'rsatish va sortirovka qilish
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True).order_by('name'),
        empty_label="--- Mahsulotni tanlang ---",
        widget=forms.Select(attrs={'class': 'form-select product-select'})
    )

# Buyurtma elementlari uchun formset yaratamiz
OrderItemFormSet = inlineformset_factory(
    Order,              # Asosiy model
    OrderItem,          # Bog'langan model
    form=OrderItemForm, # Foydalanadigan forma
    extra=1,            # Boshida 1 ta bo'sh forma ko'rsatish
    can_delete=True,    # Formalarni o'chirish imkoniyatini berish
    max_num=20          # Maksimal 20 ta buyurtma elementi (ehtiyojga qarab o'zgartiring)
)