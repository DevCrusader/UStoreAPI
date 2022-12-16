from django.db.models import Q
from customer.models import Customer


def customer_search(
        last_name: str = "*",
        first_name: str = "*",
        patronymic: str = "*"
):
    return Customer.objects.filter(
        Q(last_name__startswith=last_name[:6] if last_name != "*" else "")
        & Q(first_name__startswith=first_name[:6] if first_name != "*" else "")
        & Q(patronymic__startswith=patronymic[:6] if patronymic != "*" else "")
    ).order_by(
        "last_name"
        if last_name != "*" else "first_name"
        if first_name != "*" else "patronymic"
    )
