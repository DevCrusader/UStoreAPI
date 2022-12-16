from django.core.exceptions import ValidationError
from django.db import models

from .product import Product
from .size import Size


class ProductItem(models.Model):
    """
    Model related with Product model.
    Contains information about the product's item,
    Example:
        Shirt(Product): (ProductItems)
                        > Red shirt - S, M
                        > Blue shirt - L, XL
                        > Yellow shirt - M
    It include:
        product:    foreign key to Product model.
        type:       required string field with max_length = 100,
                    contains information about the product's item type.
        sizes:      Many-To-Many field with Size model, can be blank,
                    contains information about the product's item sizes.
                    If the related product have_size = False, then that field
                    will remain field.
        actual:     required boolean field, contains information about
                    the product's item state:
                        True - item will be displayed in store
                        False - item will not be displayed in store
        stock:      required boolean field, contains information about
                    the product's item state in stock:
                        True - item is in stock and the customer can buy it.
                        False - item is out of stock and thc customer can not buy it.
        created_date:
                    datetime field, contains information about the
                    day of product's item creating.
        updated_date:
                    datetime field, contains information about the
                    last day of product's item editing.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, null=False, blank=False)
    sizes = models.ManyToManyField('Size', blank=True)
    actual = models.BooleanField(default=True, null=False, blank=False)
    stock = models.BooleanField(default=True, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'
        ordering = ['-created_date']
        unique_together = [
            ["product", "type"]
        ]

    def add_size(self, size: str) -> None:
        """
        Adds size if the related product have_size.
        """
        if not self.product.have_size:
            raise ValidationError(f'Error in the product-item #{self.id}. '
                                  f'The related product can not be sized')
        size_ = Size.objects.filter(size=size).first()
        if size_ is None:
            raise ValidationError("Product does not have a specified size")
        self.sizes.add(size_)
        self.save()

    def remove_size(self, size: str) -> None:
        """
        Removes size from the item's sizes list.
        """
        size_ = self.sizes.filter(size=size).first()
        if size_ is None:
            raise ValidationError('Product does not have a specified size')
        self.sizes.remove(size_)
        self.save()

    def check_size(self, size: str | None) -> bool:
        """
        Checks size in sizes list of the product-item.
        If the product-item can have sizes -> search.
        If the product-item can NOT have sizes ->
            returns True only in case when requested size is None.
        """
        if self.product.have_size:
            return self.sizes.filter(size=size).exists()
        return size is None

    def size_list(self) -> list[str]:
        """
        Return the product item's sizes list.
        """
        if self.product.have_size:
            return [s.size for s in self.sizes.all()]

    def is_actual(self):
        """
        Returns the item's state.
            True in case, when actual field is True and the item has at least one photo.
        """
        return self.actual and self.productphoto_set.all().exists()

    def set_actual(self):
        """
        Sets the item's actual field to True.
        """
        if self.actual:
            raise ValidationError("The item's actual state is already True.")
        self.actual = True
        self.save()

    def set_hidden(self):
        """
        Seta the item's actual field to False.
        """
        if not self.actual:
            raise ValidationError("The item's actual state is already False.")
        self.actual = False
        self.save()

    def product_info(self):
        """
        Returns the related product's name, price, collection and description.
        """
        return {
            "id": self.product.id,
            "name": self.product.name,
            "price": self.product.price,
            "description": self.product.description,
            "collection": self.product.collection.name,
        }

    def preview_photo(self):
        preview_photo = self.productphoto_set.filter(preview=True).first()

        if preview_photo is None:
            return "There is not preview photo."

        return preview_photo.path()

    def main_photo(self):
        main_photo = self.productphoto_set \
            .exclude(preview=True) \
            .order_by("created_date") \
            .first()

        if main_photo is None:
            return "There is not even one photo."

        return main_photo.path()

    def photos(self):
        """
        Return full photo-path list from the related
        ProductPhoto model exclude preview photo.
        """
        return [
            photo.path()
            for photo in
            self.productphoto_set
            .exclude(preview=True)
            .order_by("created_date")
        ]

    def product_name(self):
        return f"{self.product.collection.name} - {self.product.name} - {self.type}"

    def __str__(self):
        return f"{self.product.collection.name} - {self.product.name} - {self.type}"
