from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Order
from customer.serializers import OrderWithProductListSerializer
from customer.utils import paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin__get_orders(request):
    """
    Returns a list of orders to the admin page using paginator.

    GET parameters:
        If state:
            accepted -> orders with state "Accepted"
            completed -> orders with state "Completed"
            canceled -> orders with state "Canceled"
            any -> all orders

        date_order:     "asc" or "desc" - order by created_date
        page:           number of in order paginator
        per_page:       number of orders in page in order paginator

    Available only for customers with admin permission.
    """
    if not request.user.customer.admin_permission:
        return Response({"error": f"Not enough rights."}, status=403)

    ordering = request.GET.get("ordering", "desc")
    state = request.GET.get("state", "Any")

    try:
        filter_query = {
            "Accepted": Q(state="Accepted"),
            "Completed": Q(state="Completed"),
            "Canceled": Q(state="Canceled"),
            "Any": Q(),
        }[state]
    except KeyError:
        return Response({
            "error": "Invalid order-state GET parameter. "
                     "it can only take the values: "
                     "Accepted, Completed, Cancelled or Any."
        }, status=400)
    else:
        result = paginator_imitation(
            Order.objects
            .filter(filter_query)
            .order_by(f"{'-' if ordering == 'desc' else ''}created_date"),
            request.GET.get("page", 1), request.GET.get("per-page", 10)
        )

        return Response(OrderWithProductListSerializer(
            result, many=True
        ).data)
