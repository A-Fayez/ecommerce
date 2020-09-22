from django.contrib import admin
from .models import (
    Category,
    MenuItem,
    ShoppingCart,
    CartItem,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
