from django.db import models


class Size(models.Model):
    """
    Model contain product's sizes.
    It includes:
        size:       required string field
    """
    size = models.CharField(max_length=5, null=False, blank=False)

    def __str__(self):
        return f"Size {self.size}"

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
