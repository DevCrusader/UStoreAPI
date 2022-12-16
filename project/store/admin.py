from django.contrib import admin

from store.models import Collection, Product, ProductItem, ProductPhoto


# Register your models here.
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_date")
    list_display_links = ("id", "name", )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("collection_name", "id", "name", "price", "have_size", "is_actual", "created_date", "updated_date")
    list_display_links = ("id", "name", )
    empty_value_display = "--empty--"


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "id", "type", "size_list", "actual", "stock", "created_date", "updated_date")
    list_display_links = ("id", "type")
    empty_value_display = "--empty--"


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ("product_item_name", "id", "path", "preview", "created_date", "updated_date")
    list_display_links = ("id", "path")
    empty_value_display = "-empty-"
