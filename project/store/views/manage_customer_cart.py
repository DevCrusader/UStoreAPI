from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.serializers import CustomerCartStoreSerializer


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_customer_cart(request, pk):
    """
    Manages the cart-item.
    Case POST request:
        Changes the cart-item's count depending on requested action.
    Case DELETE request:
        Deletes the cart-item.
    """
    if pk is None or not pk.isdigit():
        return Response("Cart-item id must be integer field.", status=400)

    cart_item = request.user.customer.cart_set.filter(id=pk).first()

    if cart_item is None:
        return Response("Desired cart item does not exist.", status=400)

    if request.method == "POST":
        action = request.data.get("action")
        if action != "add" and action != "remove":
            return Response("Unavailable action.", status=400)
        if action == "remove" and cart_item.count == 1:
            return Response("The quantity cannot be less than zero.", status=400)
        cart_item.change_count(action)

    if request.method == "DELETE":
        cart_item.delete()

    return Response(CustomerCartStoreSerializer(cart_item, many=False).data)
