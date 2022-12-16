from django.core.exceptions import ValidationError
from django.db import models
from .customer import Customer


class BalanceReplenishment(models.Model):
    """
    Model related Many-To-Many with Customer model.
    Contains information about the customer balance replenishments.
    It includes:
        customer:   foreign key to Customer model, show who exactly
                    WAS replenished ucoins.
                    related_name - incoming_balance_replenishments_set
        from_customer:
                    foreign key to Customer model, show who exactly
                    replenished ucoins.
                    related_name - outgoing_balance_replenishments_set
        count:      positive integer field, contains the count of ucoins
                    for which the balance was replenished.
        comment:    string integer field with max_length = 250.
        date:       datetime field.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name="incoming_balance_replenishments_set")
    from_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,
                                      help_text="Покупатель, который начислил юкойны на баланс.",
                                      related_name="outgoing_balance_replenishments_set")
    count = models.PositiveIntegerField(null=False)
    comment = models.TextField(max_length=250, null=False, blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пополнение баланса"
        verbose_name_plural = "Пополнения балансов"
        ordering = ["-date"]

    def __str__(self):
        return f"Пополнение счёта пользователя {self.customer.name()} на {self.count}"

    def customer_name(self):
        return self.customer.name()

    def from_customer_name(self):
        if self.from_customer:
            return self.from_customer.name()
        return None

    def save(self, *args, **kwargs):
        try:
            self.customer.increase_balance(self.count)
        except ValidationError as err:
            raise err
        else:
            super(BalanceReplenishment, self).save(*args, **kwargs)
