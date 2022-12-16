from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Customer
from customer.serializers import CustomerExtendedSerializer


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def admin__delete_customer(request, pk):
    """
    Deletes the searched customer by primary key.

    Available only for customers with admin permission.
    """

    if not request.user.customer.admin_permission:
        return Response({"error": "Not enough permissions."}, status=403)

    if pk is None or not pk.isdigit():
        return Response({"error": "Customer id must be integer field."}, status=400)

    # Case when customer delete himself
    if request.user.id == int(pk):
        return Response({"error": "You can't delete your own account."}, status=400)

    customer = Customer.objects.filter(id=pk).first()

    # Check that desired customer exists
    if customer is None:
        return Response({"error": "Desired customer does not exist."}, status=400)

    customer.user.delete()
    customer.delete()

    return Response(CustomerExtendedSerializer(customer).data, status=200)

