from django.contrib import admin
from .models import User,Fan,Customer,Product,Order,OrderItem,ShippingAddress

# Register your models here.

admin.site.register(User)
admin.site.register(Fan)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)