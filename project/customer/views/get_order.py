from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Order
from customer.serializers import OrderWithProductListSerializer


@api_view(["GET"])
def get_order(request, pk):
    """
    Returns the order by requested primary key.
    """
    order = Order.objects.filter(id=pk).first()

    if pk is None or not pk.isdigit():
        return Response({"error": "Order id must be integer field."}, status=400)

    # Проверяет, существует ли искомый по ключу заказ
    if order is None:
        return Response({"error": "Desired order does not exist."}, status=400)

    return Response(OrderWithProductListSerializer(order, many=False).data)
