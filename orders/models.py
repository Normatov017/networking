# orders/models.py
from django.db import models
from customers.models import Customer # Mijoz modelini import qilamiz
from products.models import Product   # Mahsulot modelini import qilamiz
from decimal import Decimal # Decimal sonlar bilan ishlash uchun

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Kutilmoqda'),       # O'zbekcha tarjimalarni berdim
        ('Processing', 'Qayta ishlanmoqda'),
        ('Shipped', 'Jo\'natildi'),
        ('Delivered', 'Yetkazib berildi'),
        ('Cancelled', 'Bekor qilindi'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL, # Mijoz o'chirilganda buyurtma o'chirilmasin
        null=True,                 # Ma'lumotlar bazasida null bo'lishi mumkin
        blank=True,                # Formada bo'sh bo'lishi mumkin
        related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending') # Status tanlovi
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # Dastlabki qiymat
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        customer_name = f"{self.customer.first_name} {self.customer.last_name}" if self.customer else "Noma'lum mijoz"
        return f"Buyurtma #{self.id} - {customer_name} - {self.order_date.strftime('%Y-%m-%d')}"

    def update_total_amount(self):
        """Buyurtma elementlarining umumiy summasini hisoblab, total_amountni yangilaydi."""
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = Decimal(str(total)) # Decimalga aylantirish muhim
        self.save()

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-order_date'] # Eng yangi buyurtmalar birinchi ko'rinsin

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL, # Mahsulot o'chirilganda buyurtma elementida qolsin (null bo'lib)
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1) # Musbat butun son
    price = models.DecimalField(max_digits=10, decimal_places=2) # Mahsulotni buyurtma qilingan vaqtdagi narxi

    def __str__(self):
        product_name = self.product.name if self.product else "Noma'lum mahsulot"
        return f"{product_name} x {self.quantity}"

    def get_total_price(self):
        """Buyurtma elementining umumiy narxini qaytaradi."""
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        """
        Agar narx kiritilmagan bo'lsa, mahsulotning joriy narxini oladi.
        """
        if not self.price and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"