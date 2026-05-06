from django.urls import path
from . import views

urlpatterns = [

    # HOME (MARKETPLACE)
    path('', views.home, name='home'),

    # MAP PAGE
    path('map/', views.map_view, name='map'),

    # AUTH
    path('register/', views.register_view, name='register'),

    # SHOP SETUP / UPDATE PROFILE
    path('shop/', views.register_shop, name='register_shop'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # PRODUCTS (PRICES)
    path('add-price/', views.add_price, name='add_price'),

    path('edit/<int:price_id>/', views.edit_price, name='edit_price'),
    path('delete/<int:price_id>/', views.delete_price, name='delete_price'),

    # CHAT SYSTEM
    path('chat/<int:shop_id>/', views.chat, name='chat'),

    # PAYMENT SYSTEM
    path('pay/', views.pay_subscription, name='pay'),

    # DELETE SHOP
    path('delete-shop/', views.delete_shop, name='delete_shop'),

    # ONLINE STATUS (REAL-TIME AJAX)
    path('set-online/', views.set_online, name='set_online'),
]