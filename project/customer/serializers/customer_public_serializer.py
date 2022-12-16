from rest_framework import serializers

from customer.models import Customer


class CustomerPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    Contains information about customer's public info.
    It includes:
        id:         ID of the customer.
        name:       string field, name of the customer.
    """
    class Meta:
        model = Customer
        fields = ("id", "name")
