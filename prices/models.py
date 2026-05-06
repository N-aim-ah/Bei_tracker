from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator


# ==============================
# VALIDATION
# ==============================
kenya_phone_validator = RegexValidator(
    regex=r'^(?:2547\d{8}|2541\d{8})$',
    message="Use Kenya format: 254712345678"
)


# ==============================
# SHOP
# ==============================
class Shop(models.Model):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')

    name = models.CharField(max_length=150)

    location_name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    phone = models.CharField(max_length=12, validators=[kenya_phone_validator])
    email = models.EmailField(blank=True)

    business_image = models.ImageField(upload_to='shop_images/', blank=True, null=True)

    is_paid = models.BooleanField(default=False)
    subscription_end = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    # 🔥 REAL-TIME STATUS
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seller')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.is_active

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.phone}" if self.phone else None


# ==============================
# PRICE / PRODUCTS
# ==============================
class Price(models.Model):

    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('electronics', 'Electronics'),
        ('clothes', 'Clothes'),
        ('other', 'Other'),
    )

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='prices')

    item_name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='food')

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('shop', 'item_name')

    def __str__(self):
        return self.item_name


# ==============================
# CHAT
# ==============================
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ==============================
# PAYMENT
# ==============================
class Payment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=500)
    paid_at = models.DateTimeField(auto_now_add=True)