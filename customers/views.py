# customers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer 
from .forms import CustomerForm

def customer_list(request):
    customers = Customer.objects.all().order_by('last_name', 'first_name')
    return render(request, 'customers/customer_list.html', {'customers': customers})
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mijoz muvaffaqiyatli qo\'shildi!')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Yangi Mijoz Qo\'shish'})
        

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.info(request, 'Mijoz muvaffaqiyatli yangilandi!')
            return redirect('customers:customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Mijozni Tahrirlash'})
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.warning(request, 'Mijoz muvaffaqiyatli o\'chirildi!')
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})