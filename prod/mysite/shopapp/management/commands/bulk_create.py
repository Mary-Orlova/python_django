from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order, Product
from typing import Sequence


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        self.object = self.get_object()

        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.only('id').all()
        order, created = Order.objects.get_or_create(
            delivery_address='ul Serova, d 28',
            promocode='promo5',
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f'Created order {order}')
