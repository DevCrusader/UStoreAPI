from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Gift
from customer.serializers import ExtendedGiftSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer__accept_gift(request, pk):
    gift = request.user.customer.incoming_gift_set\
        .filter(Q(state=Gift.GiftState.Sent) & Q(id=pk)).first()

    if gift is None:
        return Response({
            "detail": "The desired gift is already accepted or does not exist."
        }, status=400)

    gift.accept()

    return Response(ExtendedGiftSerializer(gift, many=False).data)
