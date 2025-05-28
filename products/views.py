# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm # Yangi formani import qilamiz
from django.contrib import messages # Xabar chiqarish uchun

def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli qo\'shildi!')
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Yangi Mahsulot Qo\'shish'})
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Mahsulot muvaffaqiyatli yangilandi!')
            return redirect('products:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Mahsulotni Tahrirlash'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.warning(request, 'Mahsulot muvaffaqiyatli o\'chirildi!')
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})