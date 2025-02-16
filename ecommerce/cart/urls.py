# cart/urls.py
from django.urls import path
from . import views
from .views import add_address
from .views import checkout, payment, order_confirmation
from .views import mark_order_shipped
from .views import order_detail
from .views import cancel_order

app_name = "cart"

urlpatterns = [
    path("", views.cart_view, name="cart_view"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", checkout, name="checkout"),
    path("add-address/", views.add_address, name="add_address"),
    path("payment/<int:order_id>/", payment, name="payment"),  # Add this line
    path("order-confirmation/<int:order_id>/", order_confirmation, name="order_confirmation"),
    path("review-order/", views.review_order, name="review_order"),
    path("mark-shipped/<int:order_id>/", mark_order_shipped, name="mark_shipped"),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
]
