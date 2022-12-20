from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import \
    PureBalanceWriteOffSerializer, \
    PureOrderSerializer, \
    OrderWithProductListSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer__create_order(request):
    """
    Created a customer order.
    The POST request must include:
        address -> delivery address of the order
        paymentMethod -> payment_method of the order
    """
    address = request.data.get("address")

    # Check office
    if address is None:
        return Response({"error": "Address is missing."}, status=400)

    payment_method = request.data.get('paymentMethod')

    # Проверяет, что переданный метод оплаты валидный
    if payment_method not in ["rubles", "ucoins"]:
        return Response(
            {'error': "Not valid payment method, "
                      "can be \"rubles\" or \"ucoins\"."},
            status=400
        )

    # Проверяет, что в корзине пользователя существуют item's
    if not len(request.user.customer.cart_set.all()):
        return Response({"error": "User's cart does not have any item."}, status=500)

    total_count = request.user.customer.cart_total_count()

    # Если метод оплаты - юкоины, то проверяет
    if payment_method == "ucoins":
        if total_count > request.user.customer.balance:
            return Response({"error": "Not enough ucoins"}, status=400)

    serializer = PureOrderSerializer(data={
        "customer": request.user.customer.id,
        "payment_method": payment_method,
        "address": address,
    })

    if serializer.is_valid():
        order = serializer.save()
        order.set_product_list(request.user.customer.extract_cart())
        request.user.customer.clear_cart()

        if order.payment_method == "ucoins":
            serializer = PureBalanceWriteOffSerializer(data={
                "customer": request.user.customer.id,
                "from_customer": request.user.customer.id,
                "header": f"Покупка мерча, заказ #{order.id}",
                "comment": order.products_str(),
                "count": total_count
            })

            if serializer.is_valid():
                serializer.save()

        return Response(
            OrderWithProductListSerializer(
                order, many=False
            ).data)
    return Response(serializer.errors, status=500)

