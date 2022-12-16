from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Order
from customer.serializers import OrderWithProductListSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin__change_order_state(request, pk):
    """
    Searched the requested order py primary key and changes state.
    The POST request must include:
        state -> new state of the order

    Available only for customers with admin permission.
    """

    # Проверяет, достаточно ли у пользователя прав для данного действия
    if not request.user.customer.admin_permission:
        return Response({"error": f"Not enough rights."}, status=403)

    if pk is None or not pk.isdigit():
        return Response({"error": "Order id must be integer field."}, status=400)

    order = Order.objects.filter(id=pk).first()

    # Проверяет, существует ли заказ по переданному запросу
    if order is None:
        return Response({"error": f"Desired order does not exist."}, status=400)

    state = request.data.get("state")

    if state not in Order.OrderStateChoice.values:
        return Response({"error": "Incorrect new state"}, status=400)

    order.set_state(state)
    return Response(OrderWithProductListSerializer(order).data, status=200)
