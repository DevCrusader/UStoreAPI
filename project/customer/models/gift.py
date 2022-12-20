from django.db import models

from customer.models import Customer


class Gift(models.Model):
    """
    Model related Many-To-Many with Customer model.
    Contains information about gifts of the customers.
    It includes:
        from_customer:
                    foreign key to Customer model, who send gift.
                    related_name - incoming_balance_replenishments_set
        to_customer:
                    foreign key to Customer model, who accept gift.
                    related_name - outgoing_balance_replenishments_set
        count:      positive integer field, count of gifted ucoins.
        comment:    string integer field with max_length = 250.
        created_date:
                    datetime field.
    """
    from_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        null=True, related_name="outgoing_gift_set"
    )

    to_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        null=True, related_name="incoming_gift_set"
    )

    count = models.PositiveSmallIntegerField(default=1, null=False)
    comment = models.CharField(max_length=250, null=False, blank=False)

    class GiftState(models.TextChoices):
        Sent = "Sent"
        Accepted = "Accepted"

    state = models.TextField(
        max_length=len(GiftState.Accepted), choices=GiftState.choices,
        default=GiftState.Sent, null=False, blank=False
    )

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"

    def __str__(self):
        return f"Подарок от {self.from_customer.name()}"

    def accept(self):
        self.state = self.GiftState.Accepted
        self.save()

    def from_customer_name(self):
        return self.from_customer.name()

    def to_customer_name(self):
        return self.to_customer.name()
