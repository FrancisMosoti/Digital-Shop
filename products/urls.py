from django.urls import path
from . import views as my_views

urlpatterns = [
    path('', my_views.products, name='products'),
    path('add-products/', my_views.add_products, name='add-products'),
    path('all-products/', my_views.products, name='products'),
    path('update-products/', my_views.update_products, name='update-products'),
]
