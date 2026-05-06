from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from datetime import timedelta
from math import radians, cos, sin, sqrt, atan2

from .forms import RegisterForm, ShopForm, ShopUpdateForm
from .models import Shop, Price, Message, Payment


# ==============================
# DISTANCE CALCULATION (GPS)
# ==============================
def distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# ==============================
# HOME (MARKET + SEARCH + NEAREST)
# ==============================
def home(request):
    query = request.GET.get('q')
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')

    prices = Price.objects.select_related('shop').all()

    if query:
        prices = prices.filter(item_name__icontains=query)

    if user_lat and user_lng:
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)

            prices = sorted(
                prices,
                key=lambda p: distance(
                    user_lat,
                    user_lng,
                    p.shop.latitude or 0,
                    p.shop.longitude or 0
                )
            )
        except:
            pass

    return render(request, "home.html", {
        "prices": prices,
        "query": query
    })


# ==============================
# MAP VIEW
# ==============================
def map_view(request):
    shops = Shop.objects.all()
    return render(request, "map.html", {"shops": shops})


# ==============================
# REGISTER USER + AUTO SHOP
# ==============================
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

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
# DASHBOARD
# ==============================
@login_required
def dashboard(request):
    shop = Shop.objects.filter(owner=request.user).first()

    if not shop:
        shop = Shop.objects.create(
            owner=request.user,
            name=f"{request.user.username}'s Shop",
            location_name="Not set",
            latitude=-4.0435,
            longitude=39.6682,
            phone="",
            email=request.user.email
        )

    prices = Price.objects.filter(shop=shop)

    return render(request, "dashboard.html", {
        "shop": shop,
        "prices": prices
    })


# ==============================
# SHOP PROFILE EDIT (FIXED + MERGED)
# ==============================
@login_required
def register_shop(request):
    shop = Shop.objects.filter(owner=request.user).first()

    if request.method == "POST":
        form = ShopUpdateForm(request.POST, request.FILES, instance=shop)

        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            messages.success(request, "Shop updated successfully.")
            return redirect('dashboard')

    else:
        form = ShopUpdateForm(instance=shop)

    return render(request, "register_shop.html", {"form": form})


# ==============================
# ADD PRODUCT
# ==============================
@login_required
def add_price(request):
    shop = get_object_or_404(Shop, owner=request.user)

    if request.method == "POST":
        item_name = request.POST.get('item_name')
        amount = request.POST.get('amount')
        image = request.FILES.get('image')

        Price.objects.create(
            shop=shop,
            item_name=item_name,
            amount=amount,
            image=image
        )

        messages.success(request, "Product added successfully.")
        return redirect('dashboard')

    return render(request, "price.html")


# ==============================
# EDIT PRODUCT
# ==============================
@login_required
def edit_price(request, price_id):
    price = get_object_or_404(Price, id=price_id, shop__owner=request.user)

    if request.method == "POST":
        price.item_name = request.POST.get('item_name')
        price.amount = request.POST.get('amount')

        if request.FILES.get('image'):
            price.image = request.FILES.get('image')

        price.save()
        messages.success(request, "Product updated successfully.")
        return redirect('dashboard')

    return render(request, "edit_price.html", {"price": price})


# ==============================
# DELETE PRODUCT
# ==============================
@login_required
def delete_price(request, price_id):
    price = get_object_or_404(Price, id=price_id, shop__owner=request.user)

    if request.method == "POST":
        price.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('dashboard')

    return render(request, "confirm_delete_price.html", {"price": price})


# ==============================
# DELETE SHOP
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
    messages_list = Message.objects.filter(shop=shop)

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
# PAYMENT SYSTEM
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


# ==============================
# ONLINE STATUS
# ==============================
@login_required
def set_online(request):
    shop = Shop.objects.filter(owner=request.user).first()

    if shop:
        shop.is_online = True
        shop.last_seen = timezone.now()
        shop.save()

    return JsonResponse({"status": "ok"})
#