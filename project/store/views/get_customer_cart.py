from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.serializers import CustomerCartStoreSerializer
from customer.models import Customer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_customer_cart(request):
    """
    Returns the list of customer's cart-items.
    """
    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        return Response(
            {'error': f"User {request.user.username} "
                      f"does not have related customer."},
            status=400)

    return Response(
        CustomerCartStoreSerializer(
            customer.cart_set.all(),
            many=True
        ).data
    )
