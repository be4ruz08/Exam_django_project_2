from django.contrib import admin
from django.urls import path
from shop.views import product_list, product_detail, order_add, comment_add, home, about

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('category/<slug:category_slug>/', home, name='products_by_category'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('order/add/', order_add, name='order_add'),
    path('add_comment/<int:product_id>/', comment_add, name='add_comment'),
]

