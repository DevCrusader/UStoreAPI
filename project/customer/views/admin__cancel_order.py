from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Order
from customer.serializers import \
    PureBalanceReplenishmentSerializer, \
    OrderWithProductListSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin__cancel_order(request, pk):
    """
    Cancels the requested order by primary key.

    Available only for customers with admin permission.
    """
    # Проверяет права юзера
    if not request.user.customer.admin_permission:
        return Response({"error": "Not enough rights."}, status=403)

    if pk is None or not pk.isdigit():
        return Response({"error": "Order id must be integer field."}, status=400)

    order = Order.objects.filter(id=pk).first()

    # Проверяет, что искомы заказ существует
    if order is None:
        return Response({"error": "Desired order does not exists."}, status=400)

    comment = request.data.get("comment")

    if comment is None or len(comment) == 0:
        return Response({"detail": "Cancellation reason is required."}, status=400)

    if len(str(comment)) > 200:
        return Response({"detail": "Comment field can not have more than 200 characters."}, status=400)

    # Если заказ был оплачечн юкойнами то возвращает средства юзеру
    if order.payment_method == "ucoins":
        total_count = sum([item["count"] * item["price"] for item in order.products()])

        serializer = PureBalanceReplenishmentSerializer(data={
            "customer": order.customer.id,
            "from_customer": request.user.customer.id,
            "header": f"Отмена заказа #{order.id}.",
            "comment": comment,
            "count": total_count
        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=500)

        serializer.save()

    order.cancel(comment)
    return Response(OrderWithProductListSerializer(order, many=False).data)
