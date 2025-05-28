# warehouses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction # Atomik operatsiyalar uchun

# Barcha modellar import qilinganiga ishonch hosil qiling
from .models import Warehouse, Inventory, StockIn, StockOut
# Barcha formalar import qilinganiga ishonch hosil qiling
from .forms import WarehouseForm, InventoryFormSet, StockInForm, StockOutForm
from products.models import Product # Mahsulot ma'lumotini olish uchun


# --- Warehouse (Ombor) Boshqaruvi ---

@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all().order_by('name')
    context = {
        'warehouses': warehouses,
        'title': 'Omborlar Roʻyxati',
        'page_title': 'Omborlar' # Navigatsiya uchun
    }
    return render(request, 'warehouses/warehouse_list.html', context)

@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        formset = InventoryFormSet(request.POST, prefix='inventory_items') # prefix muhim

        if form.is_valid() and formset.is_valid():
            with transaction.atomic(): # Barcha operatsiyalarni bitta tranzaksiya ichida saqlash
                warehouse = form.save(commit=False)
                warehouse.save() # Warehouse'ni saqlaymiz, chunki Inventory itemlar unga bog'liq

                # Inventory itemlarni saqlash
                # Formset.save() metodini chaqirishdan oldin uning instance'ini o'rnatamiz
                # Agar formset yangi bo'lsa (instance berilmagan bo'lsa), shunday qilish kerak
                formset.instance = warehouse
                formset.save() # Bu yangi itemlarni qo'shadi va o'chirilganlarni o'chiradi

            messages.success(request, 'Ombor va inventar ma\'lumotlari muvaffaqiyatli qo\'shildi!')
            return redirect('warehouses:warehouse_list')
        else:
            messages.error(request, 'Formada xatoliklar mavjud. Iltimos, tekshiring.')
    else:
        form = WarehouseForm()
        formset = InventoryFormSet(prefix='inventory_items') # prefix muhim

    # JavaScript uchun mahsulotlar ro'yxatini JSON formatida tayyorlaymiz
    products = Product.objects.filter(is_active=True).values('id', 'name')

    context = {
        'form': form,
        'formset': formset,
        'title': 'Yangi Ombor Qo\'shish',
        'page_title': 'Yangi Ombor' # Navigatsiya uchun
        # 'products_json': list(products) # Hozircha bu yerda Product narxi kerak emas
    }
    return render(request, 'warehouses/warehouse_form.html', context)

@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    # related_name='inventories' bo'lsa, warehouse.inventories.all() ishlatiladi
    # Agar modelda related_name belgilangan bo'lmasa, default _set ishlatiladi
    inventory_items = warehouse.inventories.all().order_by('product__name') # related_name: 'inventories'
    context = {
        'warehouse': warehouse,
        'inventory_items': inventory_items,
        'title': f"{warehouse.name} Ombori",
        'page_title': f"{warehouse.name} Ombori" # Navigatsiya uchun
    }
    return render(request, 'warehouses/warehouse_detail.html', context)

@login_required
def warehouse_update(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        formset = InventoryFormSet(request.POST, instance=warehouse, prefix='inventory_items')

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                warehouse = form.save()
                formset.save() # Inventory itemlarni saqlash va o'chirish
            messages.info(request, 'Ombor ma\'lumotlari va inventar muvaffaqiyatli yangilandi!')
            return redirect('warehouses:warehouse_detail', pk=pk)
        else:
            messages.error(request, 'Formada xatoliklar mavjud. Iltimos, tekshiring.')
    else:
        form = WarehouseForm(instance=warehouse)
        formset = InventoryFormSet(instance=warehouse, prefix='inventory_items') # Mavjud elementlar bilan to'ldirish

    # products = Product.objects.filter(is_active=True).values('id', 'name') # JS uchun mahsulotlar ro'yxati

    context = {
        'form': form,
        'formset': formset,
        'title': 'Ombor ma\'lumotlarini tahrirlash',
        'page_title': f"{warehouse.name} Tahrirlash" # Navigatsiya uchun
        # 'products_json': list(products)
    }
    return render(request, 'warehouses/warehouse_form.html', context) # Shu formani qayta ishlatamiz

@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.delete()
        messages.warning(request, 'Ombor va unga bog\'liq barcha inventar ma\'lumotlari muvaffaqiyatli o\'chirildi!')
        return redirect('warehouses:warehouse_list')
    context = {
        'warehouse': warehouse,
        'title': 'Omborni o\'chirish',
        'page_title': 'Omborni o\'chirish'
    }
    return render(request, 'warehouses/warehouse_confirm_delete.html', context)


# --- StockIn (Kirim) Boshqaruvi ---

@login_required
def stock_in_create(request):
    if request.method == 'POST':
        form = StockInForm(request.POST)
        if form.is_valid():
            stock_in = form.save(commit=False)
            stock_in.save() # Signal Inventory ni avtomatik yangilaydi
            messages.success(request, 'Mahsulot omborga muvaffaqiyatli qabul qilindi!')
            return redirect('warehouses:stock_in_list')
        else:
            messages.error(request, 'Xatolik yuz berdi. Iltimos, formani to\'g\'ri to\'ldiring.')
    else:
        form = StockInForm()

    context = {
        'form': form,
        'title': 'Mahsulot kirimi',
        'page_title': 'Yangi Kirim Yaratish'
    }
    return render(request, 'warehouses/stock_in_form.html', context)

@login_required
def stock_in_list(request):
    stock_ins = StockIn.objects.all()
    context = {
        'stock_ins': stock_ins,
        'title': 'Kirimlar Roʻyxati',
        'page_title': 'Omborga Kirimlar'
    }
    return render(request, 'warehouses/stock_in_list.html', context)

# --- StockOut (Chiqim) Boshqaruvi ---

@login_required
def stock_out_create(request):
    if request.method == 'POST':
        form = StockOutForm(request.POST)
        if form.is_valid():
            stock_out = form.save(commit=False)
            # Chiqimdan oldin omborda mahsulot miqdorini tekshirish
            try:
                inventory = Inventory.objects.get(
                    warehouse=stock_out.warehouse,
                    product=stock_out.product
                )
                if inventory.quantity < stock_out.quantity:
                    messages.error(request, f'Omborda yetarli {stock_out.product.name} ({inventory.quantity} ta) mavjud emas!')
                    return render(request, 'warehouses/stock_out_form.html', {'form': form, 'title': 'Mahsulot chiqimi', 'page_title': 'Yangi Chiqim Yaratish'})
            except Inventory.DoesNotExist:
                messages.error(request, f'Bu omborda {stock_out.product.name} mavjud emas!')
                return render(request, 'warehouses/stock_out_form.html', {'form': form, 'title': 'Mahsulot chiqimi', 'page_title': 'Yangi Chiqim Yaratish'})

            stock_out.save() # Signal Inventory ni avtomatik yangilaydi
            messages.success(request, 'Mahsulot ombordan muvaffaqiyatli chiqarildi!')
            return redirect('warehouses:stock_out_list')
        else:
            messages.error(request, 'Xatolik yuz berdi. Iltimos, formani to\'g\'ri to\'ldiring.')
    else:
        form = StockOutForm()

    context = {
        'form': form,
        'title': 'Mahsulot chiqimi',
        'page_title': 'Yangi Chiqim Yaratish'
    }
    return render(request, 'warehouses/stock_out_form.html', context)

@login_required
def stock_out_list(request):
    stock_outs = StockOut.objects.all()
    context = {
        'stock_outs': stock_outs,
        'title': 'Chiqimlar Roʻyxati',
        'page_title': 'Ombordan Chiqimlar'
    }
    return render(request, 'warehouses/stock_out_list.html', context)

# --- Inventory (Inventar) Boshqaruvi ---

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all().order_by('warehouse__name', 'product__name')
    context = {
        'inventories': inventories,
        'title': 'Inventarlar Roʻyxati',
        'page_title': 'Ombor Inventarlari'
    }
    return render(request, 'warehouses/inventory_list.html', context)