from io import BytesIO

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q

from .customer import Customer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class Order(models.Model):
    """
    Model related with Customer model.
    Contains information about customer orders.
    It includes:
        customer:   foreign key to Customer model.
        product_list:
                    required bytes-like field,
                    contains the customer's product list.
        payment_method:
                    string field with choice between ucoins and rubles,
                    required, ucoins by default, contains information
                    about order payment method.
        address:    required string field with max_length = 150,
                    contain information about order delivery address.
        state:      string field with choice between Accepted,
                    Completed and Cancelled, required, Accepted by default,
                    contains information about order state.
        cancellation_reason:
                    string field with max_length = 250,
                    in case when state in not Cancelled may be null
        created_date:
                    datetime field, contain information about the day
                    of the order creating.
        updated_date:
                    datetime field, contain information about the last day
                    of the order editing.
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product_list = models.BinaryField(null=False, blank=False)

    class PaymentMethodChoice(models.TextChoices):
        ucoins = "ucoins"
        rubles = "rubles"

    payment_method = models.CharField(
        max_length=6,
        choices=PaymentMethodChoice.choices,
        default=PaymentMethodChoice.ucoins,
        null=False, blank=False
    )

    address = models.CharField(max_length=150, null=False, blank=False)

    class OrderStateChoice(models.TextChoices):
        accepted = "Accepted"
        completed = "Completed"
        canceled = "Canceled"

    state = models.CharField(
        max_length=len(OrderStateChoice.completed),
        choices=OrderStateChoice.choices,
        default=OrderStateChoice.accepted,
        null=False, blank=False
    )

    cancellation_reason = models.CharField(
        max_length=250,
        null=True,
        blank=False,
        default=None
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_date']
        constraints = [
            CheckConstraint(
                check=Q(
                    Q(state="Canceled") &
                    Q(cancellation_reason__isnull=False)
                ) | Q(
                    ~Q(state="Canceled") &
                    Q(cancellation_reason__isnull=True)
                ), name="reason_with_cancelled_state")
        ]

    def customer_name(self):
        """
        Returns the customer full name.
        """
        return self.customer.name()

    def set_state(self, state_=None):
        """
        Changes the order's state to new state.
        """
        if state_ is None:
            return

        if state_ not in self.OrderStateChoice.values:
            return

        if state_ == self.OrderStateChoice.canceled:
            raise ValidationError(
                "To set cancelled state use cancel() method."
            )

        if self.state != state_:
            self.state = state_
            self.cancellation_reason = None
            self.save()

    def cancel(self, reason: str):
        if reason is None or len(reason) == 0:
            raise ValidationError("Reason can not be empty.")
        self.state = self.OrderStateChoice.canceled
        self.cancellation_reason = reason

        self.save()

    def set_product_list(self, list_):
        """
        Changes the order's product_list to new list.
        Using JSONRenderer from rest_framework.
        """
        self.product_list = JSONRenderer().render(list_)
        self.save()

    def products(self):
        """
        Method parses the product_list bytes-like field to list.
        Using the JSONParser from rest_framework.
        """
        return JSONParser().parse(BytesIO(self.product_list))

    def total_count(self):
        return sum(map(
            lambda product: product["price"] * product["count"],
            self.products()
        ))

    def products_str(self):
        return ", ".join([
            " ".join(
                [
                    product['name'], product['type'],
                    product['item_size']
                    if product['item_size'] is not None else '',
                    str(product['count']), 'шт.'
                ]
            ) for product in self.products()
        ])
