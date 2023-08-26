from django.contrib import admin

from api.models import Order, Payment, CreditCard, EBTCard

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ("id", "last_4", "brand", "exp_month", "exp_year")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_total", "status", "success_date")

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "payment_method", "status", "success_date")

class EBTCardAdmin(admin.ModelAdmin):
    list_display = ("id", "last_4", "brand")

admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(EBTCard, EBTCardAdmin)