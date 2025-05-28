# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views # views.py dan home_view, dashboard_view va API views ni import qilamiz
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'), # Bosh sahifa URL
    path('dashboard/', views.dashboard_view, name='dashboard'), # Statistika paneli URL

    # Ilova URL'lari
    path('products/', include('products.urls')),
    path('customers/', include('customers.urls')),
    path('orders/', include('orders.urls')),
    path('warehouses/', include('warehouses.urls')),

    # AUTHENTIFICATION URL'LARI
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # Statistika API URL'lari (diagrammalar uchun ma'lumotlar)
    path('api/daily-sales/', views.daily_sales_api, name='daily_sales_api'),
    path('api/top-products/', views.top_products_api, name='top_products_api'),
]

# Mahalliy rivojlanish uchun statik fayllarni qo'llab-quvvatlash
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)