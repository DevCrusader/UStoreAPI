from rest_framework import serializers

from customer.models import Order


class OrderSimplifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "state",
            "address",
            "total_count",
            "products_str",
            "updated_date",
        )
