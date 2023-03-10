from django.contrib.auth.backends import BaseBackend
from customer.models import Customer, SecretWord


class ExtendBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        username = username.split(" ")

        if len(username) != 3:
            return None

        ln, fn, p = username
        if password and username:
            try:
                customer = Customer.objects.get(
                    first_name=fn,
                    last_name=ln,
                    patronymic=p)
                if SecretWord.objects.first().check_secret_word(password):
                    return customer.user
            except Customer.DoesNotExist:
                return None
        return None
