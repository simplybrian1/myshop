from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import json
from .models import Cart, CartItem
from products.models import Product
from .models import Order, OrderItem
from .utils import send_order_email

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        session_cart_id = request.session.get("cart_id")
        if session_cart_id:
            session_cart = Cart.objects.filter(id=session_cart_id, user=None).first()
            if session_cart:
                for item in session_cart.items.all():
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
                    if not created:
                        cart_item.quantity += item.quantity
                    cart_item.save()
                session_cart.delete()
            request.session["cart_id"] = None
    else:
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id, user=None)
        if created:
            request.session["cart_id"] = cart.id
    return cart

@login_required
def cart_view(request):
    cart = get_cart(request)
    return render(request, "cart/cart_view.html", {"cart": cart})

@login_required
def add_to_cart(request, product_id):
    cart = get_cart(request)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect("cart:cart_view")
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect("cart:cart_view")

@login_required
def remove_from_cart(request, item_id):
    cart = get_cart(request)
    CartItem.objects.filter(id=item_id, cart=cart).delete()
    return redirect("cart:cart_view")

from django.shortcuts import render, redirect, get_object_or_404
from .models import Address, Order

def checkout(request):
    if request.method == "POST":
        address_id = request.POST.get("address")
        
        if not address_id:
            return render(request, "cart/checkout.html", {"error": "No address selected!"})

        try:
            address = Address.objects.get(id=address_id, user=request.user)  # Ensure the address belongs to the user
        except Address.DoesNotExist:
            return render(request, "cart/checkout.html", {"error": "Selected address does not exist!"})

        # Process order (assuming you have logic for this)
        order = Order.objects.create(user=request.user, address=address)

        # Redirect to order confirmation page
        return redirect("cart:order_confirmation", order_id=order.id)

    addresses = Address.objects.filter(user=request.user)
    
    if not addresses.exists():
        return render(request, "cart/checkout.html", {"error": "You have no saved addresses. Please add one!"})

    return render(request, "cart/checkout.html", {"addresses": addresses})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Address
from .forms import AddressForm  # We'll create this form next

@login_required

def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = AddressForm()
    return render(request, 'cart/add_address.html', {'form': form})

@login_required
def checkout(request):
    if request.method == "POST":
        address_id = request.POST.get("address")
        
        if not address_id:
            return render(request, "cart/checkout.html", {"error": "Please select an address."})

        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Store selected address in session
        request.session["checkout_address"] = address_id

        return redirect("cart:review_order")  # Proceed to order review

    addresses = Address.objects.filter(user=request.user)  # Make sure this is fetching addresses
    print(addresses)  # Debugging line

    return render(request, "cart/checkout.html", {"addresses": addresses})



@login_required
def review_order(request):
    cart = get_cart(request)
    address_id = request.session.get("checkout_address")

    if not address_id:
        return redirect("cart:checkout")  # Redirect back if no address selected

    address = Address.objects.get(id=address_id, user=request.user)

    if request.method == "POST":
        # Create the order
        order = Order.objects.create(user=request.user, address=address, status="pending")

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Clear the cart after placing the order
        cart.items.all().delete()

        return redirect("cart:order_confirmation", order_id=order.id)

    return render(request, "cart/review_order.html", {"cart": cart, "address": address})


@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "cart/order_confirmation.html", {"order": order})

from django.shortcuts import render

def pay_deposit_via_mpesa(request):
    # TODO: Implement M-Pesa payment logic
    return render(request, "cart/mpesa_payment.html")
@login_required
def order_tracking(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "cart/order_tracking.html", {"orders": orders})
@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "cart/payment.html", {"order": order})
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def mark_order_shipped(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "pending":  # Ensure it's a valid status transition
        order.status = "shipped"
        order.save()

       # Send shipment email
        subject = "Order Shipped"
        message = f"Your order #{order.id} has been shipped! It will arrive soon."
        send_order_email(subject, message, order.user.email)    
    
    return redirect('profile')  # Redirect to profile page after marking as shipped
from django.shortcuts import render, get_object_or_404
from .models import Order

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'order_detail.html', {'order': order})
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == "Pending":
        order.status = "Cancelled"
        order.save()

        # Send cancellation email
        subject = "Order Cancelled"
        message = f"Your order #{order.id} has been cancelled."
        send_order_email(subject, message, order.user.email)

    return redirect("profile")

from django.shortcuts import render, redirect
from .models import Order, CartItem
from .utils import send_order_email

def checkout(request):
    if request.method == "POST":
        # Get the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return redirect("cart")  # Redirect if cart is empty

        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total_price=sum(item.product.price * item.quantity for item in cart_items),
            status="Pending"
        )

        # Move cart items to the order
        for item in cart_items:
            order.items.add(item)  # Assuming you have a ManyToMany relation
            item.delete()  # Remove item from cart after adding to order

        # Send order confirmation email
        subject = "Order Placed Successfully"
        message = f"Your order #{order.id} has been placed successfully. Thank you for shopping with us!"
        send_order_email(subject, message, request.user.email)

        return redirect("order_confirmation", order.id)

    return render(request, "cart/checkout.html")
  