from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Customer
from customer.serializers import CustomerPublicSerializer


@api_view(['GET'])
def get_admins(request):
    """
    Returns the list of customers that have admin permission.
    """
    return Response(CustomerPublicSerializer(
        Customer.objects.filter(admin_permission=True),
        many=True
    ).data)
