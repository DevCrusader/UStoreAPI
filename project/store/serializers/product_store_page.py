from rest_framework import serializers

from store.models import Product


class ProductStorePageSerializer(serializers.ModelSerializer):
    """
    Serializer to store page.
    It includes fields:
        collection_id:
                    ID of the related Collection model.
        collection_name:
                    name of the related Collection model.
        id:         ID of the product.
        name:       name of the product.
        price:      price of the product.
        photo_list: list of paths to preview photos of the product items.
    """
    class Meta:
        model = Product
        fields = (
            "collection_id",
            "collection_name",
            "id",
            "name",
            "price",
            "photo_list"
        )
