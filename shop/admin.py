from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Wishlist, WishlistItem, Review, OrderHistory, Shipping

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'available')
    list_filter = ('available', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('price', 'quantity', 'available')

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ('product',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'fullname', 'address', 'status', 'created_at', 'tracking_id')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username', 'fullname')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'created_at')

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    raw_id_fields = ('product',)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    inlines = [WishlistItemInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('user__username', 'order__order_id')

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'address', 'city', 'postal_code', 'country', 'tracking_number', 'shipped_at', 'delivered_at')
    search_fields = ('order__order_id', 'address', 'city', 'postal_code', 'country', 'tracking_number')
    list_filter = ('shipped_at', 'delivered_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(Shipping, ShippingAdmin)
