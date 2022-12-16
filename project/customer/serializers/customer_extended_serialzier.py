from rest_framework import serializers

from customer.models import Customer


class CustomerExtendedSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    Contains information about customer's extended info, for admins only.
    It includes:
        id:         ID of the customer.
        name:       string field, name of the customer.
        balance:    positive integer field, balance of the customer.
        admin_permission:
                    boolean field, contains information about
                    the customer's admin permission.
    """
    class Meta:
        model = Customer
        fields = ("id", "name", "balance", "admin_permission")
