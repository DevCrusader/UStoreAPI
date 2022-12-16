from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import UcoinRequest
from customer.serializers import UcoinRequestWithCustomerNameSerializer
from customer.utils import paginator_imitation


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer__get_ucoin_requests(request):
    state = request.GET.get("state", "Any")
    ordering = request.GET.get("ordering", "desc")

    try:
        filters = {
            "Sent": Q(state=UcoinRequest.StateChoice.sent),
            "Rejected": Q(state=UcoinRequest.StateChoice.rejected),
            "Accepted": Q(state=UcoinRequest.StateChoice.accepted),
            "Any": Q(),
        }[state]
    except KeyError:
        return Response(
            {"detail": "The desired state filter does not exist."},
            status=400
        )
    else:
        paginated = paginator_imitation(
            request.user.customer.ucoinrequest_set.filter(filters).order_by(
                f"{'-' if ordering == 'desc' else ''}created_date"),
            request.GET.get("page", 1), request.GET.get("per-page", 10))

        return Response(
            UcoinRequestWithCustomerNameSerializer(paginated, many=True).data
        )
