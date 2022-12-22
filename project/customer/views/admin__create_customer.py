from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Customer
from customer.serializers import \
    PureCustomerSerializer, \
    PureUserSerializer, \
    CustomerPublicSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin__create_customer(request):
    """
    Creates new user and related customer.
    The POST request must include:
        lastName -> the customer's last_name
        firstName -> the customer's first_name
        patronymic -> the customer's patronymic
        balance -> the customer's balance
        permission -> the customer's permission
    Created new user with:
        username: [last_name] [first_name] [patronymic]
        password: [last_name] [first_name] [patronymic]

    Available only for customers with admin permission.
    """

    # Check requested user role
    if not request.user.customer.admin_permission:
        return Response({"error": "Not enough permissions."}, status=403)

    # Check that the request contain all fields
    missing_fields = []
    for field in [
        "lastName", "firstName", "patronymic",
        "balance", "permission"
    ]:
        if request.data.get(field) is None:
            missing_fields.append(field)

    # Response error if some field is missing
    if missing_fields:
        return Response({
            "detail": f"The request does not contain fields: {', '.join(missing_fields)}"
        }, status=400)

    # Get fields from request
    last_name = request.data.get('lastName').strip()
    first_name = request.data.get('firstName').strip()
    patronymic = request.data.get('patronymic').strip()

    existed_customer = Customer.objects.filter(first_name=first_name,
                                               last_name=last_name,
                                               patronymic=patronymic).first()

    if existed_customer is not None:
        return Response({
            "detail": "User with requested params already exists. "
                      "If you still want to register, try to change some param."
        }, status=400)

    balance = request.data.get('balance', 0.0)
    permission = request.data.get('permission')

    # Create User Serializer
    username = " ".join([last_name, first_name, patronymic])

    user_serializer = PureUserSerializer(data={
        'username': username,
        'password': username
    })

    if user_serializer.is_valid():
        user = user_serializer.save()

        # Create Customer Serializer
        customer_serializer = PureCustomerSerializer(data={
            "user": user.id,
            "first_name": first_name,
            "last_name": last_name,
            "patronymic": patronymic,
            "balance": balance,
            "admin_permission": permission
        })

        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            return Response(CustomerPublicSerializer(customer, many=False).data)

        # Response 500 if there are some error in customer serializer
        return Response(customer_serializer.errors, status=500)

    # Response 500 if there are some error in user serializer
    return Response(user_serializer.errors, status=500)
