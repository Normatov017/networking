# warehouses/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Warehouse, Inventory, StockIn, StockOut # StockIn va StockOut ni ham import qiling
from products.models import Product

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'capacity_sqm', 'contact_person', 'phone_number', 'email', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ombor nomi'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ombor manzili'}),
            'capacity_sqm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Sig\'imi (kv.m)'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mas\'ul shaxs'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqami'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Ombor nomi',
            'location': 'Manzil',
            'capacity_sqm': 'Sig\'imi (kv.m)',
            'contact_person': 'Mas\'ul shaxs',
            'phone_number': 'Telefon raqami',
            'email': 'Email',
            'is_active': 'Faol',
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select inventory-product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control inventory-quantity', 'min': '0'}),
        }
        labels = {
            'product': 'Mahsulot',
            'quantity': 'Miqdor',
        }

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True).order_by('name'),
        empty_label="--- Mahsulotni tanlang ---",
        widget=forms.Select(attrs={'class': 'form-select inventory-product-select'})
    )

InventoryFormSet = inlineformset_factory(
    Warehouse,
    Inventory,
    form=InventoryForm,
    extra=1,
    can_delete=True,
    max_num=50,
    validate_max=True
)

# --- Yangi qo'shiladigan formalar ---
class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ['warehouse', 'product', 'quantity', 'reason']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misol: Yetkazib beruvchidan qabul qilingan'}),
        }
        labels = {
            'warehouse': 'Ombor',
            'product': 'Mahsulot',
            'quantity': 'Miqdor',
            'reason': 'Sabab',
        }

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = ['warehouse', 'product', 'quantity', 'reason']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misol: Mijozga sotildi, qaytarildi'}),
        }
        labels = {
            'warehouse': 'Ombor',
            'product': 'Mahsulot',
            'quantity': 'Miqdor',
            'reason': 'Sabab',
        }