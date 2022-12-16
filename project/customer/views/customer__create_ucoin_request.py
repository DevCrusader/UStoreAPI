from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import PureUcoinRequestSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer__create_ucoin_request(request):
    """
    Creates the customer's ucoin-request.
    The POST request must include:
        header - string non-empty field with max_length=100
        comment - string non-empty field with max_length=250
    """
    header = request.data.get("header")

    # Validate header POST field
    if header is None:
        return Response({"detail": "Header field is missing."}, status=400)

    if type(header) is not str and len(header) > 100 and not header:
        return Response({
            "detail": "The passed header field must be a non-empty string "
                      "and its length must not exceed 100 characters."
        }, status=400)

    comment = request.data.get("comment")

    # Validate comment POST field
    if comment is None:
        return Response({"detail": "Comment field is missing."}, status=400)

    if type(comment) is not str and len(comment) > 250 and not comment:
        return Response({
            "detail": "The passed comment field must be a non-empty string "
                      "and its length must not exceed 250 characters."
        }, status=400)

    # Create serializer
    serializer = PureUcoinRequestSerializer(data={
        "customer": request.user.customer.id,
        "header": header,
        "comment": comment
    })

    if serializer.is_valid():
        u_request = serializer.save()
        return Response(PureUcoinRequestSerializer(u_request, many=False).data)

    # Return 500 error in case of serializer error
    return Response(serializer.error, status=500)
