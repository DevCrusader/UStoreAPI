from rest_framework import serializers

from store.models import Product, Cart

# Contains pure serializers.


class PureProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class PureCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
