from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib import messages
from shop.forms import OrderForm, ReviewForm
from .decorators import redirect_authenticated_user, login_required_user
from .models import Order, OrderItem, Product, Cart, CartItem, Category,Wishlist,WishlistItem, Review
# Create your views here.

@login_required_user
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})

#index view
def index(request):
    return render(request, 'shop/index.html')

def mobilephone(request):
    category = get_object_or_404(Category, name="Mobile Phones")
    category_description = category.description
    products = Product.objects.filter(category=category)
    return render(request, 'shop/mobilephone.html', {'products': products, 'category_description': category_description})

def laptop(request):
    category = get_object_or_404(Category, name="Laptops")
    category_description = category.description
    products = Product.objects.filter(category=category)
    return render(request, 'shop/laptop.html', {'products': products, 'category_description': category_description})

def tablet(request):
    category = get_object_or_404(Category, name="Tablets")
    category_description = category.description
    products = Product.objects.filter(category=category)
    return render(request, 'shop/tablet.html' ,{'products': products, 'category_description': category_description})

def accessories(request):
    category = get_object_or_404(Category, name="Accessories")
    category_description = category.description
    products = Product.objects.filter(category=category)
    return render(request, 'shop/accessories.html', {'products': products, 'category_description': category_description})

#product detail view with product_id as parameter to get the product object and display the product details or 404 page if product not found
def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    reviews = Review.objects.filter(product=product)
    
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'shop/product_detail.html', {'product': product, 'reviews': reviews})

#create the register view using shop/register.html template
@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})
#create a login view using shop/login.html template
@redirect_authenticated_user
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})
#create logout 
@login_required_user
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required_user
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if product.quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = 1
            messages.success(request, f"Added {product.name} to your cart.")
        else:
            if cart_item.quantity < product.quantity:
                cart_item.quantity += 1
                messages.success(request, f"Updated quantity for {product.name}.")
            else:
                messages.error(request, f"Cannot add more {product.name}. Only {product.quantity} in stock.")
                return redirect('cart')
        cart_item.save()
    else:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('cart')
    
    return redirect('cart')
    
@login_required_user
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'shop/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })
@login_required_user
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required_user
def clear_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.clear()
    return redirect('cart')
    
@login_required_user
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'processing'
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                item.product.quantity -= item.quantity
                item.product.save()

            cart.clear()
            return redirect('order_success', order_id=order.order_id)
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

@login_required_user
def order_success(request, order_id):
    if request.user != Order.objects.get(order_id=order_id).user:
        return redirect('index')
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

@login_required_user
def wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.products.all()
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required_user
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    return redirect('wishlist')

@login_required_user
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product=product)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required_user
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user  
            new_review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', product_id=product_id)
        else:
            messages.error(request, 'There was an error submitting your review.')
    else:
        review_form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'review_form': review_form,
        'reviews': reviews,
    })

@login_required_user
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('product_detail', product_id=review.product.product_id)

    return render(request, 'shop/confirm_delete_review.html', {'review': review})

