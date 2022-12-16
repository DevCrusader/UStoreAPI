from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Order


@api_view(["GET"])
def get_new_request_count(request):
    """
    Returns the number of new requests
    """

    # FIXME
    return Response(
        len(Order.objects.filter(state=Order.OrderStateChoice.accepted))
    )
