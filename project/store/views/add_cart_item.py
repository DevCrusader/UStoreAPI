from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.models import ProductItem, Size
from store.serializers import \
    CustomerCartStoreSerializer, \
    PureCartSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cart_item(request):
    """
    Searches the requested product-item and adds it to the customer's cart.
    """
    product_id = request.data.get("productId")
    type_ = request.data.get("type")
    size = request.data.get("size")

    # Ищем доустпный товар с переданными параметрами
    product_item = ProductItem.objects.filter(product_id=product_id, type=type_).first()

    # Если такого нет, то возвращаем ошибку
    if product_item is None:
        return Response({"error": "Desired product item does not exist."}, status=400)

    # Если у товара должен быть размер, но не передан, то возвращаем ошибку
    if product_item.product.have_size and size is None:
        return Response({"error": "Product must have the size."}, status=400)

    # Если товар не имеет переданного размера, то возвращаем ошибку
    if not product_item.check_size(size):
        return Response({"error": "Product does not have this size."}, status=400)

    # Проверяет, есть ли у пользователя данный товар в корзине, если есть, то возвращает ошибку
    if request.user.customer.cart_set.filter(
            product_item=product_item,
            size=Size.objects.get(size=size) if size else None
    ).exists():
        return Response({"error": "Product is already in the cart."}, status=400)

    serializer = PureCartSerializer(data={
        "customer": request.user.customer.id,
        "product_item": product_item.id,
        "size": Size.objects.get(size=size).id if size else None
    })

    if serializer.is_valid():
        cart_item = serializer.save()
        return Response(
            CustomerCartStoreSerializer(cart_item, many=False).data
        )

    return Response(serializer.errors, status=500)
