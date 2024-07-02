from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product, Category, Order
from .forms import OrderForm, CommentForm


# Create your views here.

# @login_required
def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def products(request):
    search_query = request.GET.get('search')
    product_list = Product.objects.all()

    if search_query:
        product_list = product_list.filter(
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query))

    context = {
        'product_list': product_list,
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/detail.html', context)


def order_add(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'shop/order_form.html', {'form': form})


def comment_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            return redirect('product_detail', slug=product.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'shop/detail.html', {
        'product': product,
        'comment_form': comment_form,
    })


def home(request):
    sort = request.GET.get('sort', 'default')
    category_slug = request.GET.get('category', None)

    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if sort == 'expensive':
        products = products.order_by('-price')
    elif sort == 'cheap':
        products = products.order_by('price')
    elif sort == 'new':
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'sort': sort,
        'category': category_slug,
    }

    return render(request, 'shop/home.html', context)


def about(request):
    return render(request, 'shop/about.html')

