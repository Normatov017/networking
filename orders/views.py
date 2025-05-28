# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction # Atomik operatsiyalar uchun
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from products.models import Product # Mahsulot narxini olish uchun

def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, prefix='items') # prefix muhim
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic(): # Barcha operatsiyalarni bitta tranzaksiya ichida saqlash
                order = form.save(commit=False)
                order.save() # Orderni saqlaymiz, chunki OrderItemlar unga bog'liq bo'lishi kerak
                
                # OrderItem'larni saqlash
                for item_form in formset:
                    if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'): # Bo'sh va o'chirilgan formani saqlamaymiz
                        order_item = item_form.save(commit=False)
                        order_item.order = order
                        # Mahsulot narxini OrderItem modelining save() metodida avtomatik o'rnatiladi.
                        order_item.save()
                
                order.update_total_amount() # Umumiy summani yangilash

            messages.success(request, 'Buyurtma muvaffaqiyatli qo\'shildi!')
            return redirect('orders:order_list')
        else:
            messages.error(request, 'Formada xatoliklar mavjud. Iltimos, tekshiring.')
    else:
        form = OrderForm()
        formset = OrderItemFormSet(prefix='items') # prefix muhim
    
    # JavaScript uchun mahsulotlar ro'yxatini JSON formatida tayyorlaymiz
    products = Product.objects.filter(is_active=True).values('id', 'name', 'price') 

    context = {
        'form': form,
        'formset': formset,
        'title': 'Yangi Buyurtma Qo\'shish',
        'products_json': list(products) # JSON formatida o'tkazamiz
    }
    return render(request, 'orders/order_form.html', context)

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = order.items.all() # Buyurtmaga tegishli elementlar
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order, prefix='items')
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save()
                formset.save() # OrderItem'larni saqlash va o'chirish
                order.update_total_amount() # Umumiy summani yangilash
            messages.info(request, 'Buyurtma muvaffaqiyatli yangilandi!')
            return redirect('orders:order_detail', pk=pk)
        else:
            messages.error(request, 'Formada xatoliklar mavjud. Iltimos, tekshiring.')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order, prefix='items') # Mavjud elementlar bilan to'ldirish
    
    products = Product.objects.filter(is_active=True).values('id', 'name', 'price') # JS uchun mahsulotlar ro'yxati

    context = {
        'form': form,
        'formset': formset,
        'title': 'Buyurtmani Tahrirlash',
        'products_json': list(products)
    }
    return render(request, 'orders/order_form.html', context)

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.warning(request, 'Buyurtma muvaffaqiyatli o\'chirildi!')
        return redirect('orders:order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})