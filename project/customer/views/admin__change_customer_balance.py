from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils.translation import gettext_lazy as _

from customer.models import Customer
from customer.serializers import \
    PureBalanceReplenishmentSerializer, \
    PureBalanceWriteOffSerializer, \
    CustomerExtendedSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin__change_customer_balance(request, pk):
    """
    Changes the requested by primary key customer's balance.
    The POST request must include:
        new_balance -> the customer's new balance
        comment -> che change's commentary

    Available only for customers with admin permission.
    """
    if not request.user.customer.admin_permission:
        return Response({"detail": _("Not enough rights.")}, status=403)

    if pk is None or not pk.isdigit():
        return Response({"detail": _("Customer id must be an integer field.")},
                        status=400)

    new_balance = request.data.get("newBalance")
    comment = request.data.get("comment")

    # NewBalance field validation
    if new_balance is None:
        return Response({
            "detail": _("NewBalance parameter is missing.")
        }, status=400)

    try:
        new_balance += 0.0
    except TypeError:
        return Response({
            "detail": _(f"The passed newBalance must be an integer "
                        f"or a float, get {str(type(new_balance))} instead.")
        }, status=400)

    # Comment field validation
    if comment is None or not comment:
        return Response({"detail": "The passed comment is missing or invalid."}, status=400)

    customer = Customer.objects.filter(id=pk).first()

    if not customer:
        return Response({"detail": "Desired customer does not exist."},
                        status=400)

    if new_balance == customer.balance:
        return Response({
            "detail": "The customer already has requested balance. "
                      "Probably another administrator changed "
                      "the balance for this reason."
        }, status=400)

    # Balance change serializer data
    data = {
        "customer": customer.id,
        "from_customer": request.user.customer.id,
        "header":
            f"Пополнение от администратора {request.user.customer.name()}"
            if new_balance > customer.balance else
            f"Списание от администратора {request.user.customer.name()}",
        "comment": comment,
        "count": abs(customer.balance - new_balance)
    }

    # Create balance change serializer based on change type
    serializer = PureBalanceReplenishmentSerializer(data=data) \
        if new_balance > customer.balance else \
        PureBalanceWriteOffSerializer(data=data)

    if serializer.is_valid():
        data = serializer.save()
        # Return updated customer object
        return Response(
            CustomerExtendedSerializer(data.customer, many=False).data)

    # Return 500 in case serializer with errors
    return Response(serializer.errors, status=500)
