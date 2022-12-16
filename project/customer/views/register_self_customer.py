from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import SecretWord, Customer
from customer.serializers import \
    PureCustomerSerializer, \
    PureUserSerializer, \
    CustomerPublicSerializer


@api_view(["POST"])
def register_self_customer(request):
    """
    Allow to user's register themselves.
    The POST request must include:
        firstName -> the customer's first_name
        lastName -> the customer's last_name
        patronymic -> the customer's patronymic

        secret_word -> check secret_word

    By default, created Customer will be with:
        admin_permission: False
        balance: 0

    Created User will be with:
        username: [last_name]_[first_name]_[patronymic]
        password: [last_name]_[first_name]_[patronymic]
    """

    missing_fields = []
    for field in ["firstName", "lastName", "patronymic", "secretWord"]:
        if request.data.get(field) is None:
            missing_fields.append(field)

    if len(missing_fields) != 0:
        return Response({"detail": f"These parameters are missing: {' '.join(missing_fields)}."}, status=400)

    first_name = request.data.get("firstName")
    last_name = request.data.get("lastName")
    patronymic = request.data.get("patronymic")
    secret_word = request.data.get("secretWord")

    if not SecretWord.objects.first().check_secret_word(secret_word):
        return Response({"detail": "Incorrect secret word."}, status=400)

    customer = Customer.objects.filter(first_name=first_name, last_name=last_name, patronymic=patronymic).first()

    if customer is not None:
        return Response(
            {"detail": f"Customer {' '.join([last_name, first_name, patronymic])} already exists."},
            status=400)

    username = "_".join([last_name, first_name, patronymic])
    user_serializer = PureUserSerializer(data={
        "username": username,
        "password": username
    })

    if user_serializer.is_valid():
        user = user_serializer.save()

        customer_serializer = PureCustomerSerializer(data={
            "user": user.id,
            "first_name": first_name,
            "last_name": last_name,
            "patronymic": patronymic,
            "balance": 0,
            "admin_permission": False
        })

        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            return Response(CustomerPublicSerializer(customer, many=False).data)

        return Response(customer_serializer.errors, status=500)

    return Response(user_serializer.errors, status=500)
