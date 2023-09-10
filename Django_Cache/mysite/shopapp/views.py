"""
В этом модуле лежат различные представления.

Разные view для интернет-магазина: по товарам, заказам и тд.
"""


from timeit import default_timer

from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, response
from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from myauth.models import Profile
from .forms import ProductForm
from .models import Product, Order, ProductImage
from .serializers import OrderSerializer, ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.syndication.views import Feed


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над product
    Полрый CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    odering_fields = [
        'name',
        'price',
        'discount',
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
     summary='Get one product by ID',
     description='Retrives **product**, return 404 if not found',
     responses={
        202: ProductSerializer,
        404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['user', 'products']
    filterset_fields = [
        'delivery_address',
        'user',
        'products',
    ]
    odering_fields = [
        'delivery_address',
        'user',
        'products',
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = "name", "price", "description", "discount", 'preview'
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        if self.request.user.is_superuser and not Profile.objects.filter(user_id=1).exists():
            Profile.objects.create(user_id=1)

        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser or (self.request.user == self.get_object().created_by)
    permission_required = 'shopapp.change_product'
    model = Product
    # fields = "name", "price", "description", "discount", 'preview'
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    queryset = (
        Order
        .objects
        .select_related('user')
        .prefetch_related('products')
    )
    template_name = 'shopapp/orders-list.html'
    context_object_name = 'orders'

class UserOrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

    template_name = "shopapp/orders_user-list.html"
    context_object_name = 'owner'

    def get_queryset(self):
        # получаем пользователя по ID и фильтруем
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return self.owner


    def get_context_data(self, *, objects_list=None, **kwargs):
        # для вывода имени пользователя, заказы ктр смотрим
        context = super().get_context_data(**kwargs)
        # только выбранный пользователь по пк с загрузкой к заказу продуктов
        context['orders_list'] = (
            Order.objects
                .filter(user_id=self.owner.pk)
                .prefetch_related('products')
            )
        context['profile_id'] = Profile.objects.filter(user_id=self.owner.pk)
        return context


class UserDataExportView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:

        # создание кэш-ключa
        cache_key = f"orders_cache:{self.kwargs['user_id']}"
        orders_data = cache.get(cache_key)
        # проверка-есть ли что в кэш
        if orders_data is None:
            # вызов ошибки, если пользователь не зашел на сайт
            user = get_object_or_404(User, pk=self.kwargs['user_id'])
            # создание заказов по фильтру пользователя
            user_orders = Order.objects.order_by('-pk').filter(user=user)
            # передача данных в словарь - заказы пользователя/преобразование информации
            orders_data = OrderSerializer(user_orders, many=True)
            # установка кэш
            cache.set(cache_key, orders_data, 300)
        return JsonResponse({"orders": orders_data.data})


class OrderCreateView(CreateView):
    model = Order
    fields = 'user', 'products', 'delivery_address', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'products', 'delivery_address', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

    model = Order
    context_object_name = "order"


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_cache"
        products_data = cache.get(cache_key)

        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        return JsonResponse({'products': products_data})


class LatestProductsFeed(Feed):
    title = 'Shop (latest)'
    description = 'Updates on changes and addiction products'
    link = reverse_lazy('shopapp:products/latest/feed/')

    # Для загрузки продуктов
    def items(self):
        return (
            Product.objects
            .filter(created_at__isnull=False)
            .order_by('-created_at')[:5]
        )

    def item_title(self, item: Product):
        return item.title

    def item_description(self, item: Product):
        return item.body[:200]


class OrdersDataExportView(View):
    def test_funk(self):
        if self.request.user.is_staff:
            return self.request.user

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()

        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class LatestOrdersFeed(Feed):
    title = 'Shop (latest)'
    description = 'Updates on changes and addiction orders'
    link = reverse_lazy('shopapp:orders/latest/feed/')

    # Для загрузки заказов
    def items(self):
        return (
            Order.objects
            .filter(created_at__isnull=False)
            .order_by('-created_at')[:5]
        )

    def item_title(self, item: Order):
        return item.title

    def item_description(self, item: Order):
        return item.body[:200]