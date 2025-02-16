"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project/urls.py
from django.contrib import admin
from django.urls import path, include
from cart import views as cart_views  # Rename the import to avoid name conflicts
from users.views import home, profile_view, edit_profile  # Import necessary views
from cart.views import order_detail , cancel_order

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('users/', include('users.urls')),  # User-related URLs
    path('', home, name='home'),  # Home page
    path('cart/', include('cart.urls')),  # Cart functionality
    path('products/', include('products.urls')),  # Product listing
    path('checkout/', cart_views.checkout, name='checkout'),  # Checkout view (from cart)
    path('pay-deposit-via-mpesa/', cart_views.pay_deposit_via_mpesa, name='pay_deposit_via_mpesa'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
    # Profile URLs
    path('profile/', profile_view, name='profile'),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
