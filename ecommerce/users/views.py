from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Correct import from the products app, not users
from products.models import Product
from django.db.models import F

from products.models import Category, Product
from django.db.models import F 




def home(request):
    # Get all products with discounts
    discounted_products = Product.objects.filter(discounted_price__isnull=False)

    # Get all products for featured section (modify based on your actual filtering)
    featured_products = Product.objects.all()

    context = {
        'products': featured_products,
        'discounted_products': discounted_products,
        'categories': Category.objects.all(),
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Ensure the profile exists (it should be created via signals)
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)

            return redirect('home')  # Redirect to the home page
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # Redirect to home page after registration
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm
from .models import UserProfile
from cart.models import Order  # Ensure you're importing Order from the correct app

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    # Fetch orders and filter by status
    pending_orders = Order.objects.filter(user=request.user, status='pending') # Updated to match "processing"
    completed_orders = Order.objects.filter(user=request.user, status='shipped')  # Updated to match "shipped"

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

@login_required
def edit_profile(request):
    try:
        user_profile = request.user.profile
    except ObjectDoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        # Update profile fields
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.email = request.POST.get('email')
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.address = request.POST.get('address')

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']

        # Save the updated user profile
        user_profile.save()

        # Success message
        messages.success(request, "Your profile has been updated!")
        return redirect('profile')  # Redirect back to the profile view

    return render(request, 'users/profile.html', {'user_profile': user_profile})
from django.http import JsonResponse
from products.models import Product 

def product_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query).values('id', 'name', 'image', 'price')
    else:
        products = Product.objects.all().values('id', 'name', 'image', 'price')
    return JsonResponse(list(products), safe=False)
from django.shortcuts import render

from django.templatetags.static import static

banner_images = [
    static('images/banner1.png'),
    static('images/banner2.png'),
    static('images/banner3.png'),
]