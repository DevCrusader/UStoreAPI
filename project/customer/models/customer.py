from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


def validate_balance(number: float):
    print("NUMBER:", number)
    try:
        number += 0.0
        print("NUMBER:", number)
    except TypeError:
        ValidationError(
            _('the number must be an integer or a float, %(var_type) instead.'),
            params={'var_type': str(type(number))}
        )

    if number < 0:
        raise ValidationError(
            _('The number can not be less than 0, %(value) instead'),
            params={'value': number}
        )

    if bool(number % 0.5):
        raise ValidationError(
            _('The number must be divisible by 0.5, %(value) instead'),
            params={'value': number}
        )


class Customer(models.Model):
    """
    Model related One-To-One with User model.
    Contains information about the user as a customer.
    It includes:
        first_name: required string field with max_length = 100,
                    contains the user's first name.
        last_name:  required string field with max_length = 100,
                    contains the user's last name.
        patronymic: required string field with max_length = 100,
                    contains the user's patronymic.
        balance:    float field, contains the user's ucoins-balance,
                    by default is 0.
        admin-permissions:
                    boolean field, if True - there are rights to access the
                    admin-page of the service.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    patronymic = models.CharField(max_length=100, null=False, blank=False)
    # balance = models.PositiveSmallIntegerField(default=0)
    balance = models.FloatField(
        default=0.0,
        validators=[
            validate_balance,
            MaxValueValidator(9999.9),
            MinValueValidator(0.0)
        ],
        null=False
    )
    admin_permission = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def increase_balance(self, delta: int):
        """
        Increases the customer's balance by a delta.
        """
        self.balance += delta
        self.save()

    def decrease_balance(self, delta: int):
        """
        Decreases the customer's balance by a delta.
        Check that the balance does not fall below zero.
        """
        if self.balance < delta:
            raise ValidationError("User balance must not be negative")
        self.balance -= delta
        self.save()

    def cart_total_count(self) -> list[int]:
        """
        Returns the total price of the items in the cart.
        """
        return sum([c.price() * c.count for c in self.cart_set.all()])

    def clear_cart(self):
        """
        Clears the customer's cart.
        """
        return self.cart_set.all().delete()

    def grant_admin_permission(self):
        """
        Method grants the customer admin permission.
        """
        self.admin_permission = True
        self.save()

    def revoke_admin_permission(self):
        """
        Method revokes the customer admin permission.
        """
        self.admin_permission = False
        self.save()

    def name(self) -> str:
        """
        Join and return stripped customer name.
        """
        return " ".join(
            [self.last_name, self.first_name, self.patronymic]).strip()

    def get_incoming_balance_replenishments_history(self) -> QuerySet:
        """
        Returns the customer's incoming balance replenishments.
        """
        return self.incoming_balance_replenishments_set.all()

    def get_incoming_balance_write_offs_history(self) -> QuerySet:
        """
        Returns the customer's incoming balance write-offs.
        """
        return self.outgoing_balance_write_offs_set.all()

    def get_outgoing_balance_replenishments_history(self) -> QuerySet:
        """
        Returns the customer's outgoing balance replenishments.
        """
        return self.incoming_balance_replenishments_set.all()

    def get_outgoing_balance_write_offs_history(self) -> QuerySet:
        """
        Returns the customer's outgoing balance write-offs.
        """
        return self.outgoing_balance_write_offs_set.all()

    def extract_cart(self):
        return [
            {
                "product_id": c.product_id(),
                "name": c.name(),
                "type": c.type(),
                "item_size": c.item_size(),
                "photo": c.photo(),
                "price": c.price(),
                "count": c.count,
            } for c in self.cart_set.all()
        ]

    def order_history(self):
        return [
            {

            } for order in self.order_set.all()
        ]

    def __str__(self):
        return f"Покупатель #{self.id} {self.name()}"
