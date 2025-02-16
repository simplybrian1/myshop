# users/urls.py
from django.urls import path
from . import views
from .views import product_suggestions

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),  # Login page
    path('product-suggestions/', product_suggestions, name='product_suggestions'),
]
