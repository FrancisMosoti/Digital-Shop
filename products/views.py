
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .credentials import *
from .forms import ProductForm
from django.contrib import messages
from .models import Product


# Create your views here.
def products(request):
    all_products = Product.objects.all()
    contex = {"products": all_products}
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

    return render(request, 'products/add_products.html', {'form': form})


def update_products(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product_name = request.POST.get('name')
        product_qtty = request.POST.get('qtty')
        product_desc = request.POST.get('desc')
        product_price = request.POST.get('price')
        product_image = request.FILES.get('image')
        product.name = product_name
        product.qtty = product_qtty
        product.desc = product_desc
        product.price = product_price
        product.image = product_image
        product.save()
        messages.success(request, "Product updated successfully")
        return redirect("products")
    return render(request, 'products/updates_products.html', {'product': product})


def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect('products')


def pay(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        phone = request.POST['phone-number']
        amount = product.price
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "School fees"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("success")
    return render(request, 'products/pay.html', {'product': product})


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]
    return render(request, 'token.html', {"token": validated_mpesa_access_token})

