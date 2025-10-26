from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# create an  order OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend our Order model
class OrderAdmin(admin.ModelAdmin):
    model= Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInline]

# Unregister Order Model
admin.site.unregister(Order)

# Re-register our Order And OrderAdmin
admin.site.register(Order, OrderAdmin)