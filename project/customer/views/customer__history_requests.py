from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from customer.models import UcoinRequest
from customer.serializers import PureUcoinRequestSerializer
from customer.utils import paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__history_requests(request):
    state = request.GET.get("state", "Any")
    ordering = request.GET.get("ordering", "desc")

    try:
        filter_ = {
            "Sent": Q(state=UcoinRequest.StateChoice.sent),
            "Accepted": Q(state=UcoinRequest.StateChoice.accepted),
            "Rejected": Q(state=UcoinRequest.StateChoice.rejected),
            "Any": Q(),
        }[state]
    except KeyError:
        return Response({
            "detail": "The passed state is invalid."
        }, status=400)
    else:
        requests = paginator_imitation(
            request.user.customer.ucoinrequest_set
            .filter(filter_)
            .order_by(f"{'-' if ordering == 'desc' else ''}updated_date"),
            request.GET.get("page", "1"),
            request.GET.get("per_page", "10")
        )

        return Response(
            PureUcoinRequestSerializer(requests, many=True).data
        )
