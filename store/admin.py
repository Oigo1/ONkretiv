from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(SpecialCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

