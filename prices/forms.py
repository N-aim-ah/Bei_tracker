from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Shop


# ==============================
# USER REGISTRATION FORM
# ==============================
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# ==============================
# SHOP FORM (CREATE / BASIC EDIT)
# ==============================
class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = [
            'name',
            'location_name',
            'latitude',
            'longitude',
            'phone',
            'business_image'
        ]


# ==============================
# SHOP UPDATE FORM (FULL PROFILE EDIT)
# ==============================
class ShopUpdateForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = [
            'name',
            'location_name',
            'latitude',
            'longitude',
            'phone',
            'email',
            'business_image'
        ]