from django.shortcuts import render


# Create your views here.
def products(request):
    return render(request, 'products/products.html')


def add_products(request):
    return render(request, 'products/add_products.html')


def update_products(request):
    return render(request, 'products/updates_products.html')
