from django.core.exceptions import ValidationError
from django.db import models

from customer.models import Customer
from .product_item import ProductItem
from .size import Size


class Cart(models.Model):
    """
    Model related with Customer model.
    Contains information about the product-items that are in the customer's cart.
    It includes:
        customer:   foreign key to Customer model.
        product_item:
                    foreign key to ProductItem model.
        size:       foreign key to Size model.
        count:      required positive integer field, contains information
                    about count of the product item in the customer's cart.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, blank=True, default=None,
                             on_delete=models.SET_NULL)
    count = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиция в корзине'
        verbose_name_plural = 'Позиции в корзине'
        ordering = ['-count']

    def change_count(self, action: str) -> None:
        """
        Changes count, requested action param must be 'add' or 'remove'
        """
        if action == "add":
            if self.count < 10:
                self.count += 1
                return self.save()

        if action == "remove":
            if self.count == 1:
                raise ValidationError("The count is already 1.")
            self.count -= 1
            return self.save()

    def item_size(self):
        """
        Return size of the related ProductItem.
        """
        return self.size.size if self.size else None

    def product_id(self):
        """
        Id of the related Product model
        """
        return self.product_item.product.id

    def name(self):
        """
        Name of the related Product model
        """
        return self.product_item.product.name

    def price(self):
        """
        Price of the related Product model
        """
        return self.product_item.product.price

    def type(self):
        """
        Type of the related ProductItem
        """
        return self.product_item.type

    def photo(self):
        """
        Photo of the related ProductItem
        """
        return self.product_item.main_photo()

    def in_stock(self):
        """
        in_stock field of the related ProductItem
        """
        return self.product_item.stock
