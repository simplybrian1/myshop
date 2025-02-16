from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# View to display the product list
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Filtering by category
    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category_id=category_id)

    # Filtering by gender
    gender = request.GET.getlist("gender")  # Get multiple values
    if gender:
        products = products.filter(gender__in=gender)  # Assumes gender is a field in your model

    # Filtering by price range
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "products/product_list.html", context)

def product_detail(request, id):  # Change product_id to id
    product = get_object_or_404(Product, id=id)
    context = {"product": product}
    return render(request, "products/product_details.html", context)