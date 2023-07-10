from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from shopapp.models import Order


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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

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
                'user': order.user,
                'product': order.product,
            }
            for order in orders
        ]

        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)

