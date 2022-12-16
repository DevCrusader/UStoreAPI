from rest_framework import serializers

from customer.models import Order


class OrderWithProductListSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    Contains information about the related customer and
    the order with parsed product list.
    It includes:
        id:         ID of the order
        customer_id:
                    ID of the related customer.
        customer_name:
                    name of the related customer.
        products:   parsed product_list.
        payment_method:
                    payment_method of the order.
        address:    delivery address of the order.
        state:      current state of the order: Accepted,
                    Completed or Cancelled.
        cancellation_reason:
                    string, must be null if state is not Cancelled.
        created_date:
                    the date of the order creating.
        updated_date:
                    the last date of rhe order editing.
    """
    class Meta:
        model = Order
        fields = (
            "id",
            "customer_id",
            "customer_name",
            "products",
            "payment_method",
            "address",
            "state",
            "cancellation_reason",
            "created_date",
            "updated_date"
        )
