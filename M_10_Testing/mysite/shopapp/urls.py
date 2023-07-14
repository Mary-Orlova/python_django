from django.urls import path

app_name = 'shopapp'

from .views import (
    ShopIndexView,
    ProductDetailsView,
    ProductsListView,
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    OrderUpdateView,
    OrdersDataExportView,
    OrderDeleteView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),

    path("orders/", OrdersDataExportView.as_view(), name="orders_export"),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/',  OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/archive/', OrderDeleteView.as_view(), name='order_delete'),
]
