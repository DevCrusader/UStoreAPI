from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import \
    MyTokenObtainPairView, \
    get_admins, \
    get_order, \
    register_self_customer, \
    search_customers, \
    get_new_order_count, \
    get_new_request_count

from .views import \
    admin__get_ucoin_requests, \
    admin__change_ucoin_request_state, \
    admin__get_orders, \
    admin__change_order_state, \
    admin__cancel_order, \
    admin__search_customers, \
    admin__create_customer, \
    admin__change_customer_balance, \
    admin__change_customer_permission, \
    admin__delete_customer

from .views import \
    customer__get_balance, \
    customer__create_ucoin_request, \
    customer__create_order, \
    customer__create_gift, \
    customer__get_incoming_gifts, \
    customer__accept_gift

from .views import \
    customer__history_balance, \
    customer__history_orders, \
    customer__history_requests, \
    customer__history_gifts


urlpatterns = [
    # Paths for authorized admins
    path("admin/requests/<str:pk>/", admin__change_ucoin_request_state),
    path("admin/requests/", admin__get_ucoin_requests),

    path("admin/orders/", admin__get_orders),
    path("admin/order/<str:pk>/state/", admin__change_order_state),
    path("admin/order/<str:pk>/cancel/", admin__cancel_order),

    path("admin/customers/create/", admin__create_customer),
    path("admin/customers/", admin__search_customers),

    path("admin/customer/<str:pk>/balance/", admin__change_customer_balance),
    path("admin/customer/<str:pk>/permission/",
         admin__change_customer_permission),
    path("admin/customer/<str:pk>/delete/", admin__delete_customer),

    # Paths for authorized customers
    path("customer/balance/", customer__get_balance),

    path("customer/requests/create/", customer__create_ucoin_request),

    path("customer/orders/create/", customer__create_order),

    path("customer/gifts/create/", customer__create_gift),
    path("customer/gifts/<str:pk>/", customer__accept_gift),
    path("customer/gifts/", customer__get_incoming_gifts),

    path("customer/history/balance/", customer__history_balance),
    path("customer/history/orders/", customer__history_orders),
    path("customer/history/requests/", customer__history_requests),
    path("customer/history/gifts/", customer__history_gifts),

    # Paths for any user
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/", MyTokenObtainPairView.as_view()),

    path("admin/", get_admins),
    path("order/<str:pk>/", get_order),
    path("register/", register_self_customer),
    path("search-customers/", search_customers),
    path("new-orders/", get_new_order_count),
    path("new-requests/", get_new_request_count),
]
