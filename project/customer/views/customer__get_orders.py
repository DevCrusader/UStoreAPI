from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import OrderWithProductListSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__get_orders(request):
    """
    Returns a list of the customer orders.
    """
    return Response(
        OrderWithProductListSerializer(
            request.user.customer.order_set.all().order_by("-updated_date"),
            many=True
        ).data
    )
