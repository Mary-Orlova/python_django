from timeit import default_timer

from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, response
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from myauth.models import Profile
from .forms import ProductForm
from .models import Product, Order, ProductImage


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
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

class OrdersDataExportView(View):
    def test_funk(self):
        if self.request.user.is_staff:
            return self.request.user

    def get(self, request: HttpRequest) :
        orders = Order.objects.order_by('pk').all()

        orders_data =[
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
