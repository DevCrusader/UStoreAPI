from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product
from store.serializers import ProductProductPageSerializer


@api_view(["GET"])
def get_product__store(request, pk):
    """
    Find the product by requested primary key.
    Response contains information about the product that should
    be displayed in product page of the service.
    """
    if pk is None or not pk.isdigit():
        return Response({"error": "Product id must be integer field."}, status=400)

    product = Product.objects.filter(id=pk).first()

    if product is None:
        return Response({"error": f"Product with id {pk} does not exist."}, status=404)

    if not product.is_actual():
        return Response({"error": f"Product with id {pk} is not actual."}, status=400)

    return Response(ProductProductPageSerializer(product, many=False).data)
