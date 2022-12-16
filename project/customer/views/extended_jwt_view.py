from rest_framework_simplejwt.views import TokenObtainPairView

from customer.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Extends default TokenObtainPairView from jwt
    """
    serializer_class = MyTokenObtainPairSerializer
