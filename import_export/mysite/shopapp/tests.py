"""
Тесты для моделей shopapp.
"""


from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from .models import Order, Product


class OrderDetailView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user_test', password='qwerty123', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        permission = Permission.objects.get(codename='view_order')
        self.user.user_permissions.add(permission)
        self.order = Order.objects.create(
            delivery_address="ul Pupkina, d 8",
            promocode="SALE123",
            user=self.user,
        )

    def tearDown(self):
        self.order.delete()


class OrdersExportTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user_test', password='qwerty123', is_staff=True)
        cls.order = Order.objects.create(
            delivery_address="ul Pupkina, d 8",
            promocode="SALE123",
            user=cls.user,
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()]
            }
            for order in orders
            ]

        response_data = response.json()
        order_data = response_data['orders']
        # order_data = serializers.serialize('json', response.context['orders'])

        self.assertEqual(order_data, expected_data)
        # self.assertEqual(orders_data['orders'], expected_data)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
