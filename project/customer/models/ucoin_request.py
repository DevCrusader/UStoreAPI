from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint

from .customer import Customer, validate_balance


class UcoinRequest(models.Model):
    """
    Model related M:1 with Customer models.
    Contains information about the customers
    request to replenish the balance.
    It includes:
        customer:   related customer
        header:     request header, required string field with max_length=100
        comment:    request comment, required string field with max_length=250
        count:      request ucoin count, positive integer field, 0 by default,
                    can not be 0 if the request's state is not "Sent",
                    admin writes when request state changes.
        admin_comment:
                    written by the admin, string field with max_length=250,
                    empty by default, can not be an empty if the request's
                    state is not "Sent", admin writes when
                    request state changes.
        state:      requires string field, can take values:
                        "Sent" - default state when create
                        "Accepted" - admin accepts request and
                                     replenishes the customer's balance
                        "Rejected" - admin rejected request and
                                     writes off the customer's balance
        created_date:
                    datetime field, contain information about the day
                    of the request creating.
        updated_date:
                    datetime field, contain information about the last day
                    of the request editing.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    header = models.CharField(max_length=100, null=False, blank=False)
    comment = models.CharField(max_length=250, null=False, blank=False)

    # count = models.PositiveIntegerField(default=0)

    count = models.FloatField(
        default=0.0,
        validators=[
            validate_balance,
            MaxValueValidator(9999.9),
            MinValueValidator(0.0)
        ],
        null=False
    )
    admin_comment = models.CharField(
        max_length=250, null=False, blank=True, default=""
    )

    class StateChoice(models.TextChoices):
        sent = "Sent"
        accepted = "Accepted"
        rejected = "Rejected"

    state = models.CharField(
        max_length=len(StateChoice.rejected),
        choices=StateChoice.choices,
        default=StateChoice.sent,
        null=False, blank=False
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name()} - {self.header}"

    class Meta:
        verbose_name = "Запрос на пополнение"
        verbose_name_plural = "Запросы на пополнение"
        ordering = ["-created_date"]
        constraints = [
            CheckConstraint(
                check=models.Q(
                    ~models.Q(state="Sent") &
                    ~models.Q(admin_comment__exact="")
                ) | models.Q(
                    models.Q(state="Sent") &
                    models.Q(admin_comment__exact="")
                ),
                name="admin_comment_not_null_if_state_not_sent"
            ),
            CheckConstraint(
                check=models.Q(
                    models.Q(state="Accepted") & models.Q(count__gt=0.0)
                ) | models.Q(
                    ~models.Q(state="Accepted") & models.Q(count=0.0)
                ),
                name="count_is_not_zero_if_state_is_accepted"
            )
        ]

    def change_state(
            self, new_state: str,
            admin_comment: str | None,
            count: float | None):
        """
        Changes state of the request.

        @params: new_state -> next state
        @params: admin_comment -> can not be an empty
                                  if next state is not "Sent"
        @params: count -> can not be 0 if next state is "Accepted"


        @returns: [
            success - (bool),
            error - (str | none),
            need_to_replenish - (bool)
        ]
        """
        if self.state == new_state:
            return False, "The request already has this state.", False

        if new_state == self.StateChoice.sent:
            self.state = new_state
            self.admin_comment = ""
            self.count = 0
        elif new_state == self.StateChoice.accepted:
            if type(admin_comment) is not str:
                return False, \
                    "In case the state changes to 'Accepted' the " \
                    "passed admin_comment must be a non-empty string.", \
                    False

            if len(admin_comment) == 0 or len(admin_comment) > 250:
                return False, \
                    "The passed admin comment must be a non-empty " \
                    "string and its can not exceed 250 characters.", \
                    False

            if type(count) is not float:
                return False, \
                    "In case the state change to 'Accepted' " \
                    "count field must be a positive integer.", \
                    False

            if count <= 0:
                return False, \
                    "In case the state change to 'Accepted' " \
                    "count field must be a positive integer.", \
                    False

            self.state = new_state
            self.admin_comment = admin_comment
            self.count = count
        elif new_state == self.StateChoice.rejected:
            if type(admin_comment) is not str:
                return False, \
                    "In case the state changes to 'Rejected' the " \
                    "passed admin_comment must be a non-empty string.", \
                    False

            if len(admin_comment) == 0 or len(admin_comment) > 250:
                return False, \
                    "The passed admin comment must be a non-empty " \
                    "string and its can not exceed 250 characters.", \
                    False

            self.state = new_state
            self.admin_comment = admin_comment
            self.count = 0.0
        else:
            return False, \
                "The passed new state is invalid. " \
                "It can take values: 'Sent', 'Accepted' ,'Rejected'", \
                False

        self.save()

        return True, None, new_state == self.StateChoice.accepted

    def customer_name(self) -> str:
        return self.customer.name()
