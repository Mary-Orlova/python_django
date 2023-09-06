"""
Подключение путей для приложения shopapp.
"""


from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
    ProductsDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    LatestOrdersFeed,
)

app_name = 'shopapp'


routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path('api/', include(routers.urls)),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path('products/latest/feed/', LatestProductsFeed(), name='products_feed'),

    path("orders/", OrdersDataExportView.as_view(), name="orders_export"),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/',  OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/archive/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/latest/feed/', LatestOrdersFeed(), name='orders_feed'),
]
