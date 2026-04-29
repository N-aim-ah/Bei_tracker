from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ==============================
# SHOP (BUSINESS PROFILE)
# ==============================
class Shop(models.Model):

    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shop'
    )

    name = models.CharField(max_length=150)
    location_name = models.CharField(max_length=200)

    latitude = models.FloatField()
    longitude = models.FloatField()

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # 💳 SUBSCRIPTION
    is_paid = models.BooleanField(default=False)
    subscription_end = models.DateTimeField(null=True, blank=True)

    # 🟢 ACTIVE / INACTIVE BUSINESS
    is_active = models.BooleanField(default=True)

    # 👤 ROLE
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='seller'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # ⏳ CHECK SUBSCRIPTION STATUS
    def is_subscription_active(self):
        if self.subscription_end:
            return self.subscription_end > timezone.now()
        return False

    # 🟢 CHECK IF SHOP IS AVAILABLE
    def is_available(self):
        return self.is_active and self.is_subscription_active()


# ==============================
# ITEMS (PRODUCT LIST)
# ==============================
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==============================
# PRICES (PRODUCT PRICING)
# ==============================
class Price(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='prices'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(
        upload_to='items/',
        blank=True,
        null=True
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - KES {self.amount}"


# ==============================
# CHAT SYSTEM
# ==============================
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"


# ==============================
# PAYMENT SYSTEM
# ==============================
class Payment(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.PositiveIntegerField(default=500)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shop.name} - KES {self.amount}"