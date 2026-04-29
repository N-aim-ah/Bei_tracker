from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .forms import RegisterForm
from .models import Shop, Item, Price, Message, Payment


# ==============================
# HOME
# ==============================
def home(request):
    prices = Price.objects.select_related('item', 'shop').order_by('-date')
    return render(request, "home.html", {"prices": prices})


# ==============================
# MAP
# ==============================
def map_view(request):
    shops = Shop.objects.all()
    return render(request, "map.html", {"shops": shops})


# ==============================
# REGISTER (AUTO CREATE SHOP)
# ==============================
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Auto create shop
            Shop.objects.create(
                owner=user,
                name=f"{user.username}'s Shop",
                location_name="Not set",
                latitude=-4.0435,
                longitude=39.6682,
                phone="",
                email=user.email
            )

            login(request, user)
            return redirect('dashboard')

    return render(request, "register.html", {"form": form})


# ==============================
# LOGIN
# ==============================
class CustomLoginView(LoginView):
    template_name = "login.html"


# ==============================
# LOGOUT
# ==============================
def logout_view(request):
    logout(request)
    return redirect('home')


# ==============================
# DASHBOARD (SELLER PANEL)
# ==============================
@login_required
def dashboard(request):
    shop = get_object_or_404(Shop, owner=request.user)
    prices = Price.objects.filter(shop=shop).select_related('item')

    return render(request, "dashboard.html", {
        "shop": shop,
        "prices": prices
    })


# ==============================
# ADD PRICE
# ==============================
@login_required
def add_price(request):
    shop = get_object_or_404(Shop, owner=request.user)

    # Block unpaid users
    if not shop.is_paid:
        return render(request, "blocked.html")

    items = Item.objects.all()

    if request.method == "POST":
        item_id = request.POST.get('item')
        amount = request.POST.get('amount')
        image = request.FILES.get('image')  # optional

        if not item_id or not amount:
            messages.error(request, "All fields are required.")
            return redirect('add_price')

        item = get_object_or_404(Item, id=item_id)

        Price.objects.create(
            item=item,
            shop=shop,
            amount=amount,
            image=image
        )

        messages.success(request, "Price added successfully.")
        return redirect('dashboard')

    return render(request, "price.html", {"items": items})


# ==============================
# DELETE SHOP (NEW)
# ==============================
@login_required
def delete_shop(request):
    shop = get_object_or_404(Shop, owner=request.user)

    if request.method == "POST":
        shop.delete()
        messages.success(request, "Your business has been deleted.")
        return redirect('home')

    return render(request, "confirm_delete.html", {"shop": shop})


# ==============================
# CHAT SYSTEM
# ==============================
@login_required
def chat(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    messages_list = Message.objects.filter(shop=shop).select_related('sender')

    if request.method == "POST":
        content = request.POST.get('message')

        if content:
            Message.objects.create(
                sender=request.user,
                shop=shop,
                content=content
            )

    return render(request, "chat.html", {
        "shop": shop,
        "messages": messages_list
    })


# ==============================
# PAYMENT (SIMULATED)
# ==============================
@login_required
def pay_subscription(request):
    shop = get_object_or_404(Shop, owner=request.user)

    shop.is_paid = True
    shop.subscription_end = timezone.now() + timedelta(days=30)
    shop.save()

    Payment.objects.create(shop=shop)

    messages.success(request, "Subscription activated successfully.")
    return redirect('dashboard')