from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        self.object = self.get_object()

        user = User.objects.get(pk=self.pk)
        order = Order.objects.get_or_create(
            delivery_address="ul Pravdy, d 12",
            promocode="SALE10",
            user=user,
        )
        self.stdout.write(f"Created order {order}")
