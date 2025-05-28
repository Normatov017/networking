# warehouses/models.py
from django.db import models
from django.db.models import Sum
from products.models import Product
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Warehouse(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Ombor nomi")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Manzil")
    capacity_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Sig'imi (kv.m)")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mas'ul shaxs")
    phone_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefon raqami")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ombor"
        verbose_name_plural = "Omborlar"
        ordering = ['name']


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Ombor")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Miqdor")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'warehouse')
        verbose_name = "Inventar"
        verbose_name_plural = "Inventarlar"
        ordering = ['warehouse__name', 'product__name']

    def __str__(self):
        return f"{self.product.name} ({self.warehouse.name}): {self.quantity} ta"

    # Yangilangan update_quantity metodi (bu metod signal bilan ishlatilmaydi, lekin modelda bo'lishi yaxshi)
    def update_quantity(self, amount):
        """
        Ombordagi mahsulot miqdorini yangilash.
        Mijozga sotilganda (manfiy) yoki qabul qilinganda (musbat).
        """
        if self.quantity + amount < 0:
            raise ValueError("Ombordagi mahsulot miqdori manfiy bo'lishi mumkin emas!")
        self.quantity += amount
        self.save()


# Yangi modellar: StockIn va StockOut
class StockIn(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_ins', verbose_name="Ombor")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    in_date = models.DateTimeField(auto_now_add=True, verbose_name="Kirim sanasi")
    reason = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sabab", help_text="Kirim sababi (masalan: Yetkazib beruvchidan qabul)")

    def __str__(self):
        return f"Kirim: {self.product.name} - {self.quantity} dona ({self.warehouse.name})"

    class Meta:
        verbose_name = "Kirim"
        verbose_name_plural = "Kirimlar"
        ordering = ['-in_date']


class StockOut(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_outs', verbose_name="Ombor")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    out_date = models.DateTimeField(auto_now_add=True, verbose_name="Chiqim sanasi")
    reason = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sabab", help_text="Chiqim sababi (masalan: Mijozga sotildi, qaytarildi)")

    def __str__(self):
        return f"Chiqim: {self.product.name} - {self.quantity} dona ({self.warehouse.name})"

    class Meta:
        verbose_name = "Chiqim"
        verbose_name_plural = "Chiqimlar"
        ordering = ['-out_date']


# Signals: StockIn/StockOut yaratilganda Inventory ni avtomatik yangilash

@receiver(post_save, sender=StockIn)
def update_inventory_on_stock_in(sender, instance, created, **kwargs):
    if created: # Faqat yangi StockIn obyekt yaratilganda
        inventory, created = Inventory.objects.get_or_create(
            warehouse=instance.warehouse,
            product=instance.product,
            defaults={'quantity': instance.quantity}
        )
        if not created: # Agar Inventory allaqachon mavjud bo'lsa
            inventory.quantity += instance.quantity
            inventory.save()

@receiver(post_delete, sender=StockIn)
def revert_inventory_on_stock_in_delete(sender, instance, **kwargs):
    try:
        inventory = Inventory.objects.get(
            warehouse=instance.warehouse,
            product=instance.product
        )
        if inventory.quantity >= instance.quantity: # Miqdor manfiy bo'lmasligi uchun tekshirish
            inventory.quantity -= instance.quantity
            inventory.save()
        else:
            # Agar o'chirilgan kirim miqdori inventardagi mavjud miqdordan ko'p bo'lsa
            # Bu holatda xato yuzaga kelishi mumkin, shuning uchun logga yozish tavsiya etiladi.
            # print(f"Ogohlantirish: Inventarda yetarli mahsulot yo'q, Kirimni o'chirishda muammo: {instance.product.name} at {instance.warehouse.name}")
            pass
    except Inventory.DoesNotExist:
        pass


@receiver(post_save, sender=StockOut)
def update_inventory_on_stock_out(sender, instance, created, **kwargs):
    if created: # Faqat yangi StockOut obyekt yaratilganda
        inventory, created = Inventory.objects.get_or_create(
            warehouse=instance.warehouse,
            product=instance.product,
            defaults={'quantity': 0} # Dastlabki miqdor 0, keyin ayiramiz
        )
        if not created: # Agar Inventory allaqachon mavjud bo'lsa
            # Miqdor manfiy bo'lmasligi uchun tekshirish
            if inventory.quantity >= instance.quantity:
                inventory.quantity -= instance.quantity
                inventory.save()
            else:
                # Agar chiqim miqdori inventardagi mavjud miqdordan ko'p bo'lsa
                # Bu yerda xato yuzaga kelishi mumkin, tranzaksiya boshqaruvini ko'rib chiqish kerak.
                # print(f"Xatolik: Omborda yetarli {instance.product.name} mavjud emas. Chiqim bekor qilindi.")
                # Agar xato bo'lsa, obyektni o'chirish yoki tranzaksiyani orqaga qaytarish kerak bo'ladi.
                pass # Hozircha shunchaki o'zgarishsiz qoldiramiz

@receiver(post_delete, sender=StockOut)
def revert_inventory_on_stock_out_delete(sender, instance, **kwargs):
    try:
        inventory = Inventory.objects.get(
            warehouse=instance.warehouse,
            product=instance.product
        )
        inventory.quantity += instance.quantity # O'chirilgan chiqimni qaytaramiz
        inventory.save()
    except Inventory.DoesNotExist:
        pass