from django.urls import path
from . import views

app_name = 'warehouses'

urlpatterns = [
    path('', views.warehouse_list, name='warehouse_list'),
    path('create/', views.warehouse_create, name='warehouse_create'), # YANGI
    path('<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('<int:pk>/update/', views.warehouse_update, name='warehouse_update'), # YANGI
    path('<int:pk>/delete/', views.warehouse_delete, name='warehouse_delete'), # YANGI
    # Kirim/Chiqim URL'lari (oldingi javobdan qolganlar)
    path('stock-in/add/', views.stock_in_create, name='stock_in_create'),
    path('stock-out/add/', views.stock_out_create, name='stock_out_create'),
    path('stock-ins/', views.stock_in_list, name='stock_in_list'),
    path('stock-outs/', views.stock_out_list, name='stock_out_list'),
    path('inventory/', views.inventory_list, name='inventory_list'),
]