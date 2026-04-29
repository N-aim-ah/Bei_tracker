from django.urls import path
from . import views

urlpatterns = [

    # ==============================
    # PUBLIC ROUTES
    # ==============================
    path('', views.home, name='home'),
    path('map/', views.map_view, name='map'),

    # ==============================
    # AUTHENTICATION
    # ==============================
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ==============================
    # USER DASHBOARD / FEATURES
    # ==============================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_price, name='add_price'),
    path('pay/', views.pay_subscription, name='pay'),

    # ==============================
    # BUSINESS MANAGEMENT
    # ==============================
    path('delete-shop/', views.delete_shop, name='delete_shop'),

    # ==============================
    # CHAT SYSTEM
    # ==============================
    path('chat/<int:shop_id>/', views.chat, name='chat'),
]