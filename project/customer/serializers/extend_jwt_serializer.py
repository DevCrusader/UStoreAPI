from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends default TokenObtainPairSerializer from jwt.
    Adds to token fields:
        permission: boolean fields, contains information about the customer's
                    admin permission
        balance:    positive integer field, contains information about
                    the customer's balance.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['permission'] = user.customer.admin_permission
        token['balance'] = user.customer.balance

        return token
