from django.contrib.auth.models import User
from rest_framework import serializers

from customer.models import \
    UcoinRequest, \
    Order, \
    BalanceReplenishment, \
    BalanceWriteOff, \
    Customer, \
    SecretWord, \
    Gift


# Contains pure serializers.
class PureUcoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UcoinRequest
        fields = "__all__"

class PureGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = "__all__"


class PureOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class PureBalanceReplenishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReplenishment
        fields = "__all__"


class PureBalanceWriteOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceWriteOff
        fields = "__all__"


class PureCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class PureUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PureSecretWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretWord
        fields = "__all__"
