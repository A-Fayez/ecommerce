from django.contrib import admin
from .models import (
    Category,
    MenuItem,
    Topping,
    Extra,
    ShoppingCart,
    OrderedItem,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Topping)
admin.site.register(Extra)
admin.site.register(ShoppingCart)
admin.site.register(OrderedItem)
