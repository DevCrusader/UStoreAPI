from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Customer
from customer.serializers import \
    PureBalanceReplenishmentSerializer, \
    PureBalanceWriteOffSerializer, \
    PureGiftSerializer, \
    ExtendedGiftSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer__create_gift(request):
    """
    Created gift from request customer.
    The POST data must include:
        to_customer_id - ID of the customer which will accept gift
        count - count of ucoins
        comment - comment
    """
    to_customer_id = request.data.get("to_customer_id")

    if to_customer_id is None:
        return Response({
            "detail": "to_customer_id field is missing."
        }, status=400)

    if request.user.customer.id == to_customer_id:
        return Response({
            "detail": "You can not give a gift to yourself."
        }, status=400)

    to_customer = Customer.objects.filter(id=to_customer_id).first()

    if to_customer is None:
        return Response({
            "detail": "the desired customer does not exist."
        }, status=400)

    count = request.data.get("count")

    if type(count) is not int:
        return Response({
            "detail": "The passed count field is not an integer"
        }, status=400)

    if count <= 0:
        return Response({
            "detail": "THe passed count field less or equal then zero."
        }, status=400)

    if count > request.user.customer.balance:
        return Response({
            "detail": "The passed count more than the balance of the customer."
        }, status=400)

    comment = request.data.get("comment")

    if type(comment) is not str:
        return Response({
            "detail": "The passed comment is not a string."
        }, status=400)

    if len(comment) == 0 or len(comment) > 250:
        return Response({
            "detail": "The passed comment is empty or "
                      "exceed then 250 characters."
        }, status=400)

    bwo_serializer = PureBalanceWriteOffSerializer(data={
        "customer": request.user.customer.id,
        "from_customer": request.user.customer.id,
        "header": f"Подарок для {to_customer.name()}",
        "count": count,
        "comment": comment
    })

    if not bwo_serializer.is_valid():
        return Response(bwo_serializer.errors, status=500)

    bwo_serializer.save()

    br_serializer = PureBalanceReplenishmentSerializer(data={
        "customer": to_customer.id,
        "from_customer": request.user.customer.id,
        "header": f"Подарок от {request.user.customer.name()}",
        "count": count,
        "comment": comment
    })

    if not br_serializer.is_valid():
        return Response(br_serializer.errors, status=500)

    br_serializer.save()

    gift_serializer = PureGiftSerializer(data={
        "from_customer": request.user.customer.id,
        "to_customer": to_customer.id,
        "count": count,
        "comment": comment
    })

    if gift_serializer.is_valid():
        gift = gift_serializer.save()

        return Response(ExtendedGiftSerializer(gift, many=False).data)

    return Response(gift_serializer.error, status=500)
