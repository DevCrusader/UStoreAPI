from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_permission(request):
    return Response({"message": "AIYSGDUAGSkjn!KJB@uy!@I#U"}, status=200)
