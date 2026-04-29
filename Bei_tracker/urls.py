from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from prices.views import CustomLoginView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🌐 APP ROUTES
    path('', include('prices.urls')),

    # 🔐 AUTH ROUTES
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

# 📁 MEDIA FILES (images upload)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)