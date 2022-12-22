from itertools import chain

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import CrutchBalanceSerializer
from customer.utils import paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__history_balance(request):
    state = request.GET.get("state", "Any")
    ordering = request.GET.get("ordering", "desc")

    br_list = request.user.customer.incoming_balance_replenishments_set.all() \
        if state == "Any" or state == "Replenishments" else []
    bwo_list = request.user.customer.incoming_balance_write_offs_set.all() \
        if state == "Any" or state == "Write_offs" else []

    changes = paginator_imitation(
        sorted(
            chain(br_list, bwo_list),
            key=lambda item: item.date,
            reverse=(ordering == "desc")
        ),
        request.GET.get("page", "1"),
        request.GET.get("per-page", "10"),
    )

    return Response(CrutchBalanceSerializer(changes, many=True).data)
