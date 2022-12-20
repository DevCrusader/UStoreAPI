from rest_framework import serializers

from customer.models import Gift


class ExtendedGiftSerializer(serializers.ModelSerializer):
    """
    Serializer to Gift model.
    Extends the pure serializer with fields:
        from_customer_name - name of the from_customer
        to_customer_name - name of the to_customer
    """
    class Meta:
        model = Gift
        fields = (
            "id",
            "from_customer_id",
            "from_customer_name",
            "to_customer_id",
            "to_customer_name",
            "count",
            "comment",
            "state",
            "created_date"
        )
