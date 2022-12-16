from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Collection


@api_view(["GET"])
def get_collections__store(request):
    """
    Returns the list of collections that contains at least one product.
    """
    return Response([
        c.name for c in
        Collection.objects
        .filter(product__isnull=False)
        .distinct()
    ])
