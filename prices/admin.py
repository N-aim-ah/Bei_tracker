from django.contrib import admin
from .models import Item, Shop, Price, Message, Payment

admin.site.register(Item)
admin.site.register(Shop)
admin.site.register(Price)
admin.site.register(Message)
admin.site.register(Payment)

# Register your models here.
