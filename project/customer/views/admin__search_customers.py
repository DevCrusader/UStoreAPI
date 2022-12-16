from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import CustomerExtendedSerializer
from customer.utils import customer_search, paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin__search_customers(request):
    """
    Searches customers by GET parameters.
    The GET request must include:
        firstName - the customer's first_name
        lastName - the customer's last_name
        patronymic - the customer's patronymic
    Orders the response list by first NOT "*" parameter:
        1) list_name
        2) first_name
        3) patronymic
    """
    if not request.user.customer.admin_permission:
        return Response({"detail": "Not enough permissions."}, status=403)

    fn = request.GET.get("firstName")
    ln = request.GET.get("lastName")
    p = request.GET.get("patronymic")

    if fn is None or ln is None or p is None:
        return Response({"error": "Some of requested parameters is None."},
                        status=400)

    return Response(
        CustomerExtendedSerializer(
            paginator_imitation(
                customer_search(ln, fn, p),
                request.GET.get("page", "1"),
                request.GET.get("per-page", "5")
            ), many=True).data)
