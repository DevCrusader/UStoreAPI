from django.urls import path

from .views import \
    get_collections__store, \
    get_collection__store, \
    get_product__store, \
    get_customer_cart, \
    add_cart_item, \
    manage_customer_cart

urlpatterns = [
    path("collections/", get_collections__store),
    path("products/", get_collection__store),
    path("product/<str:pk>/", get_product__store),
    path("cart/get/", get_customer_cart),
    path("cart/add/", add_cart_item),
    path("cart/manage/<str:pk>/", manage_customer_cart),
]
