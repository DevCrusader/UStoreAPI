from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from customer.models import Order
from customer.serializers import OrderSimplifySerializer
from customer.utils import paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__history_orders(request):
    state = request.GET.get("state", "Any")
    ordering = request.GET.get("ordering", "desc")

    try:
        filter_ = {
            "Accepted": Q(state=Order.OrderStateChoice.accepted),
            "Completed": Q(state=Order.OrderStateChoice.completed),
            "Canceled": Q(state=Order.OrderStateChoice.canceled),
            "Any": Q()
        }[state]
    except KeyError:
        return Response({
            "detail": "the passed state is invalid."
        }, status=400)
    else:
        orders = paginator_imitation(
            request.user.customer.order_set
            .filter(filter_)
            .order_by(f"{'-' if ordering == 'desc' else ''}updated_date"),
            request.GET.get("page", "1"),
            request.GET.get("per_page", "10")
        )

        return Response(OrderSimplifySerializer(orders, many=True).data)
