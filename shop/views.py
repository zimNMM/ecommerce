from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .decorators import redirect_authenticated_user
from .models import Product
# Create your views here.




#index view
def index(request):
    return render(request, 'shop/index.html')

def mobilephone(request):
    return render(request, 'shop/mobilephone.html')

def laptop(request):
    return render(request, 'shop/laptop.html')

def order_page(request):
    product_name = request.GET.get('product', 'Unknown Product')
    return render(request, 'order.html', {'product_name': product_name})

def process_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        product = request.POST['product']
        quantity = request.POST['quantity']
        # Process the order here (e.g., save to database, send email, etc.)
        return redirect('order_success')
    else:
        return redirect('order')
    
def order_success(request):
    return render(request, 'order_success.html')


#product detail view with product_id as parameter to get the product object and display the product details or 404 page if product not found
def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'shop/product.html', {'product': product})

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
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')
