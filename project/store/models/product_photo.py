import os
from sys import platform

from django.db import models
from django.db.models import UniqueConstraint

from django.dispatch import receiver

from .product_item import ProductItem


class ProductPhoto(models.Model):
    """
    Models related with ProductItem.
    Contains information about the item photos.
    It includes:
        product_item:
                    foreign jey to ProductItem model.
        photo:      required image field, upload images in
                    {settings.static}/images/productItemPhotos/
                    contain the item's photo.
        preview:       required boolean field, contains information about
                    the photo is preview.
                        True - the photo will be displayed in the product's card in store.
                        False - additional photo for the product page.
        created_date:
                    datetime field, contains information about the
                    day of product's item creating.
        updated_date:
                    datetime field, contains information about the
                    last day of product's item editing.
    """
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="images/productItemPhotos/")
    preview = models.BooleanField(default=False, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Фото типа товара'
        verbose_name_plural = 'Фото типов товаров'
        ordering = ["product_item", '-preview']
        constraints = [
            UniqueConstraint(
                fields=['product_item', ],
                condition=models.Q(preview=True),
                name='photo_main_constraint'
            )
        ]

    def product_item_name(self):
        return str(self.product_item)

    def path(self):
        """
        Returns the path to the photo, depending on the platform which hosts the server.
        """
        print("Platform: ", platform)
        return "/".join(self.photo.path.split("\\" if "win" in platform else "/")[-2:])

    def __str__(self):
        return f"{self.product_item.product.name} {self.product_item.type} - {'главное ' if self.preview else ''}фото"


@receiver(models.signals.post_delete, sender=ProductPhoto)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding
    'ProductPhoto' object is deleted
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(models.signals.pre_save, sender=ProductPhoto)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = ProductPhoto.objects.get(pk=instance.pk).photo
    except ProductPhoto.DoesNotExist:
        return False

    new_file = instance.photo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
