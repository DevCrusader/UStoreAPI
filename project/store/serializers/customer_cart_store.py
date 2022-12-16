from rest_framework import serializers

from store.models import Cart


class CustomerCartStoreSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model.
    It includes:
        id:         ID of the cart-item.
        count:      positive integer field.
        item_size:  string field contains information about
                    the product-item's size.
        type:       string field of the related ProductItem model
        photo:      string photo path of the related ProductItem model
        in_stock:   bool in_stock field of the related ProductItem model
        product_id: ID of the related Product model
        name:       string field of the related Product model
        price:      positive integer field of the related Product model
    """
    class Meta:
        model = Cart
        fields = (
            "id",
            "count",
            "item_size",
            "type",
            "photo",
            "in_stock",
            "product_id",
            "name",
            "price",
        )
