from rest_framework import serializers

from customer.models import UcoinRequest


class UcoinRequestWithCustomerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UcoinRequest
        fields = (
            "id",
            "header",
            "comment",
            "admin_comment",
            "count",
            "state",
            "created_date",
            "updated_date",
            "customer_id",
            "customer_name",
        )
