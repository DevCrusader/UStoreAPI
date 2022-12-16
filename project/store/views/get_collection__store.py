from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Collection
from store.serializers.product_store_page import ProductStorePageSerializer


@api_view(["GET"])
def get_collection__store(request):
    """
    Returns the products list by collection GET param.
    List contains information that should be displayed in the store page.
    """
    collection_param = request.GET.get('collection')

    if collection_param is None:
        return Response(
            {"error": "Collection get param is missing."},
            status=400
        )

    collection = Collection.objects.filter(
        name=collection_param.upper()).first()

    if collection is None:
        return Response({"error": "Collection does not exists."}, status=400)

    return Response(ProductStorePageSerializer([
        p for p in collection.product_set.all() if p.is_actual()
    ], many=True).data)
