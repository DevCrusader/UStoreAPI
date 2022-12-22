from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .customer import Customer, validate_balance


class BalanceWriteOff(models.Model):
    """
    Model related Many-To-Many with Customer model.
    Contains information about the customer balance write-offs.
    It includes:
        customer:   foreign key to Customer model, show who exactly
                    WAS written-off ucoins.
                    related_name - incoming_balance_write_offs_set
        from_customer:
                    foreign key to Customer model, show who exactly
                    written-off ucoins.
                    related_name - outgoing_balance_write_offs_set
        count:      positive integer field, contains the count of ucoins
                    for which the balance was written-off.
        comment:    string integer field with max_length = 250.
        date:       datetime field.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name="incoming_balance_write_offs_set")
    from_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,
                                      help_text="Покупатель, который списал юкойны с баланса.",
                                      related_name="outgoing_balance_write_offs_set")
    # count = models.PositiveIntegerField(default=0, null=False)
    count = models.FloatField(
        default=0.0,
        validators=[
            validate_balance,
            MaxValueValidator(9999.9),
            MinValueValidator(0.0)
        ],
        null=False
    )
    header = models.CharField(max_length=100, null=False, blank=False, default="Списание")
    comment = models.CharField(max_length=250, null=False, blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)

    type = "write_off"

    class Meta:
        verbose_name = "Списание баланса"
        verbose_name_plural = "Списания балансов"
        ordering = ["-date"]

    def __str__(self):
        return f"Списание со счёта пользователя {self.customer.name()} на {self.count}"

    def customer_name(self):
        return self.customer.name()

    def from_customer_name(self):
        if self.from_customer:
            return self.from_customer.name()
        return None

    def save(self, *args, **kwargs):
        try:
            self.customer.decrease_balance(self.count)
        except ValidationError as err:
            raise err
        else:
            super(BalanceWriteOff, self).save(*args, **kwargs)
