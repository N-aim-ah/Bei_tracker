from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from prices.views import CustomLoginView, logout_view


urlpatterns = [

    # 🔐 ADMIN PANEL
    path('admin/', admin.site.urls),

    # 🌐 ALL APP ROUTES (prices app handles everything)
    path('', include('prices.urls')),

    # 🔐 AUTH ROUTES (GLOBAL LOGIN SYSTEM)
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]


# 📁 MEDIA FILES (UPLOADS - images, shop images, product images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)