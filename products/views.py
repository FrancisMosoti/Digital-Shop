from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages
from  .models import Product


# Create your views here.
def products(request):
    all_products = Product.objects.all()
    contex = {"products":all_products}
    return render(request, 'products/products.html', contex)


def add_products(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully')
            return redirect('add-products')
        else:
            messages.error(request, "Product saving failed ")
            return redirect('add-products')
    else:
        form = ProductForm()

    return render(request, 'products/add_products.html',{'form': form})


def update_products(request):
    return render(request, 'products/updates_products.html')
