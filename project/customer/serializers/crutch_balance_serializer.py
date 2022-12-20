from rest_framework import serializers

from customer.models import BalanceReplenishment


class CrutchBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReplenishment
        fields = (
            "id",
            "header",
            "customer",
            "comment",
            "count",
            "date",
            "type"
        )
