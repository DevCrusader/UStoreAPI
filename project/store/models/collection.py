from django.db import models


class Collection(models.Model):
    """
    Contains information about the collections in the service.
    It includes:
        name:       required string field
        created_date:
                    datetime field, contains information about the day
                    of collection creating.
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

    def __str__(self):
        return self.name
