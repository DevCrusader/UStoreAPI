from django.db import models

from .collection import Collection


class Product(models.Model):
    """
    Model related with Collection Model
    Product model, contains information about product in store.
    It includes:
        collection: foreign key to Collection model, set null on delete.
        name:       required string field with max_length = 50,
                    contains the product's name.
        price:      required positive integer field,
                    contains products' price.
        description:
                    required text field with max_length = 250,
                    contains product's description.
        have_size:  required boolean field, False by default,
                    if True - the product will be able to have sizes.
        created_date:
                    datetime field, contains information about the
                    day of product creating.
        updated_date:
                    datetime field, contains information about the
                    last day of product editing.
    """
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    price = models.PositiveSmallIntegerField(default=100, null=False, blank=False)
    description = models.TextField(max_length=250, null=False, blank=True)
    have_size = models.BooleanField(default=False, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_date']

    def is_actual(self) -> bool:
        """
        Shows the product's state.
        Affect the display of the product in the store.
        Returns True in case:
            1) the product has at least one item
            2) any item is actual
        """
        if (item_list := self.productitem_set.all()).exists():
            return any([pi.is_actual() for pi in item_list])
        return False

    def items_list(self):
        """
        Returns the actual items with info of the product.
        """
        return [
            {
                'id': pi.id,
                'type': pi.type,
                'in_stock': pi.stock,
                'sizes': pi.size_list(),
                'photos': pi.photos(),
            } for pi in self.productitem_set.filter(actual=True)
        ]

    def photo_list(self):
        """
        Returns the preview photos of the product items.
        """
        return [
            pi.preview_photo()
            for pi in self.productitem_set.filter(actual=True)
        ]

    def collection_name(self):
        """
        Return the related collection's name
        """
        return self.collection.name

    def __str__(self):
        return f'{self.collection_name()} - {self.name}'
