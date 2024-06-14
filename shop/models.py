from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

#category model with name and description fields
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
#product model with category as foreign key and image field for product image upload
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=False, null=False)
    product_id = models.CharField(max_length=100, unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.product_id:
            super().save(*args, **kwargs)
            self.product_id = f'{self.category.name}{self.pk:06d}'
        super().save(*args, **kwargs)
#cart model with user as one to one field and created_at field
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.username}'

    def add_product(self, product_id, quantity):
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def remove_product(self, product_id):
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(cart=self, product=product)
        cart_item.delete()

    def clear(self):
        self.items.all().delete()

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
#cart item model with cart and product as foreign keys and quantity field
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} in cart of {self.cart.user.username}'
#order model with user as foreign key and fullname, address, created_at, status, tracking_id and order_id fields
class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f'Order {self.order_id} by {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.order_id:
            super().save(*args, **kwargs)
            self.order_id = f'ORDER{self.pk:06d}'
        super().save(*args, **kwargs)
#order item model with order and product as foreign keys and quantity field
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} in order {self.order.order_id}'
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='WishlistItem')

    def __str__(self):
        return f'Wishlist of {self.user.username}'

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} in wishlist of {self.wishlist.user.username}'
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'