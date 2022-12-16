from rest_framework import serializers

from store.models import Product


class ProductProductPageSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model to Product page.
    It includes fields:
        collection_id:
                    ID of the related Collection model.
        collection_name:
                    name of the related Collection model.
        id:         ID of the product.
        name:       name of the product.
        price:      price of the product.
        photo_list: list of paths to photos of the product items.
    """
    class Meta:
        model = Product
        fields = (
            "collection_id",
            "collection_name",
            "id",
            "name",
            "price",
            "description",
            "have_size",
            "items_list"
        )
