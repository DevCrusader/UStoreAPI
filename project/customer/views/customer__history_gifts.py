from itertools import chain

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import ExtendedGiftSerializer
from customer.utils import paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__history_gifts(request):
    state = request.GET.get("state", "Any")
    ordering = request.GET.get("ordering", "desc")

    sent = request.user.customer.outgoing_gift_set.all() \
        if state == "Sent" or state == "Any" else []
    accepted = request.user.customer.incoming_gift_set.all() \
        if state == "Accepted" or state == "Any" else []

    gifts = paginator_imitation(
        sorted(
            chain(sent, accepted),
            key=lambda item: item.created_date,
            reverse=(ordering == 'desc')
        ),
        request.GET.get("page", "1"),
        request.GET.get("per-page", "10"),
    )

    return Response(
        ExtendedGiftSerializer(gifts, many=True).data
    )
