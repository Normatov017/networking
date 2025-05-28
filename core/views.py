# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count # Ma'lumotlarni jamlash uchun
import datetime # Sana bilan ishlash uchun

# Boshqa ilovalardagi modellarni import qilish
from products.models import Product
from customers.models import Customer
from orders.models import Order, OrderItem
from warehouses.models import Warehouse, Inventory


# Bosh sahifa (login bo'lmaganlar uchun ham ko'rinishi mumkin)
def home_view(request):
    return render(request, 'home.html', {'title': 'Bosh Sahifa'})


# Statistika dashboard sahifasi (faqat login bo'lganlar uchun)
@login_required # Faqat tizimga kirgan foydalanuvchilar kira oladi
def dashboard_view(request):
    # Umumiy statistik ko'rsatkichlarni hisoblash
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    total_warehouses = Warehouse.objects.count()

    # Eng oxirgi 5 ta buyurtma
    latest_orders = Order.objects.all().order_by('-order_date')[:5]

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_warehouses': total_warehouses,
        'latest_orders': latest_orders,
        'title': 'Statistika Paneli', # Sahifa sarlavhasi
    }
    return render(request, 'dashboard.html', context)


# API endpoint: Kunlik savdo ma'lumotlari (grafik uchun)
@login_required
def daily_sales_api(request):
    today = datetime.date.today()
    # Oxirgi 30 kunlik savdo ma'lumotlarini olish
    thirty_days_ago = today - datetime.timedelta(days=30)

    sales_by_date = Order.objects.filter(order_date__gte=thirty_days_ago) \
                                 .extra(select={'day': "date(order_date)"}) \
                                 .values('day') \
                                 .annotate(total_sales=Sum('total_amount')) \
                                 .order_by('day')

    # Ma'lumotlarni JavaScript grafik kutubxonasi uchun mos formatga o'tkazish
    dates = [s['day'].strftime('%Y-%m-%d') for s in sales_by_date]
    sales = [float(s['total_sales']) for s in sales_by_date] # Decimalni floatga aylantirish

    data = {
        'labels': dates,
        'datasets': [{
            'label': 'Kunlik savdo summasi',
            'data': sales,
            'backgroundColor': 'rgba(75, 192, 192, 0.4)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'fill': True, # Chiziq ostini to'ldirish
        }]
    }
    return JsonResponse(data)


# API endpoint: Eng ko'p sotilgan mahsulotlar (grafik uchun)
@login_required
def top_products_api(request):
    # Eng ko'p sotilgan 7 ta mahsulotni miqdori bo'yicha olish
    top_products = OrderItem.objects.values('product__name') \
                                  .annotate(total_quantity_sold=Sum('quantity')) \
                                  .order_by('-total_quantity_sold')[:7]

    product_names = [p['product__name'] for p in top_products]
    product_quantities = [float(p['total_quantity_sold']) for p in top_products]

    data = {
        'labels': product_names,
        'datasets': [{
            'label': 'Sotilgan miqdor',
            'data': product_quantities,
            'backgroundColor': [
                'rgba(255, 99, 132, 0.6)',  # Red
                'rgba(54, 162, 235, 0.6)',  # Blue
                'rgba(255, 206, 86, 0.6)',  # Yellow
                'rgba(75, 192, 192, 0.6)',  # Green
                'rgba(153, 102, 255, 0.6)', # Purple
                'rgba(255, 159, 64, 0.6)',  # Orange
                'rgba(199, 199, 199, 0.6)'  # Grey
            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(199, 199, 199, 1)'
            ],
            'borderWidth': 1
        }]
    }
    return JsonResponse(data)