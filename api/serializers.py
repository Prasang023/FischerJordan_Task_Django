from rest_framework import serializers

from api.models import CreditCard, Payment, Order, EBTCard

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = [
            "id",
            "last_4",
            "brand",
            "exp_month",
            "exp_year",
        ]

class EBTCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBTCard
        fields = [
            "id",
            "last_4",
            "brand",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_total",
            "status",
            "success_date",
            "ebt_total",
        ]

class PaymentSerializer(serializers.ModelSerializer):

    payment_method = serializers.SerializerMethodField()
    def get_payment_method(self, obj):
        if isinstance(obj.payment_method, CreditCard):
            return CreditCardSerializer(obj.payment_method).data
        elif isinstance(obj.payment_method, EBTCard):
            return EBTCardSerializer(obj.payment_method).data
        else:
            return None

    class Meta:
        model = Payment
        fields = [
            "id",
            "order", # The id of the associated Order object
            "amount",
            "description",
            "payment_option",
            "payment_method_types",
            "target_id",
            "payment_method", # The id of the associated CreditCard object
            "status",
            "success_date",
            "last_processing_error"
        ]
        
