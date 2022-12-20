from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import UcoinRequest
from customer.serializers import \
    UcoinRequestWithCustomerNameSerializer, \
    PureBalanceReplenishmentSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin__change_ucoin_request_state(request, pk):
    """
    Changes state of the request by pk.
    The POST request must include:
        new_state
        count
        admin_comment
    """
    # Check admin_permission of the customer
    if not request.user.customer.admin_permission:
        return Response(
            {"error": "Only administrator can change state of the request."},
            status=400)

    # Validate the desired primeay key
    if pk is None or not pk.isdigit():
        return Response(
            {"error": "Id of the request must be an integer field."},
            status=400
        )

    _request = UcoinRequest.objects.filter(id=pk).first()

    # Check request is exist
    if _request is None:
        return Response(
            {"detail": "The desired request does not exist."},
            status=400
        )

    new_state = request.data.get("newState")
    admin_comment = request.data.get("adminComment")
    count = request.data.get("count", 0)

    # Change state of the request
    success, error, need_to_replenish = \
        _request.change_state(new_state, admin_comment, count)

    # Returns 400 with err in case of change validation error
    if not success:
        return Response({"detail": error}, status=400)

    # If changes return True, then create BalanceReplenishment
    if need_to_replenish:
        serializer = PureBalanceReplenishmentSerializer(data={
            "customer": _request.customer.id,
            "from_customer": request.user.customer.id,
            "header": f"Принят запрос #{_request.id}.",
            "count": count,
            "comment": admin_comment
        })

        if not serializer.is_valid():
            # Return 500 in case of serializer error
            return Response(serializer.errors, status=500)

        serializer.save()

    return Response(
        UcoinRequestWithCustomerNameSerializer(_request, many=False).data
    )
