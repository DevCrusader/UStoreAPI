from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Gift
from customer.serializers import ExtendedGiftSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__get_incoming_gifts(request):
    gifts = request.user.customer.incoming_gift_set.filter(state=Gift.GiftState.Sent)

    return Response(ExtendedGiftSerializer(gifts, many=True).data)
