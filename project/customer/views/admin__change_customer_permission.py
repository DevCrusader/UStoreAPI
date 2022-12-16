from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Customer
from customer.serializers import CustomerExtendedSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin__change_customer_permission(request, pk):
    """
    Changes the requested customer's by primary key admin permission.

    Available only for customers with admin permission.
    """
    if not request.user.customer.admin_permission:
        return Response(
            {"error": "Only administrator can change customer permission."},
            status=400)

    if pk is None or not pk.isdigit():
        return Response({"error": "Customer id must be integer field."},
                        status=400)

    customer = Customer.objects.filter(id=pk).first()

    if customer is None:
        return Response({"error": "Desired user does not exist."}, status=400)

    if customer.id == request.user.customer.id:
        return Response({"error": "You can't change your own role."},
                        status=400)

    permission = request.data.get("permission", False)

    if customer.admin_permission == permission:
        return Response({
            "detail": "User already have passed permission level."
                      "Probably another administrator changed "
                      "the permission level."},
            status=400)

    if permission:
        customer.grant_admin_permission()
    else:
        customer.revoke_admin_permission()

    return Response(
        CustomerExtendedSerializer(customer, many=False).data,
        status=200
    )
