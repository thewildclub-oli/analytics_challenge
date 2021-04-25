from django.test import TestCase
from .models import Order, OrderLine, ProductPromotion, VendorCommissions
from datetime import date
from django.db.models import Q

# Create your tests here.

class ChallengeTestCase(TestCase):
    """Full test case for challenge"""

    @classmethod
    def setUpTestData(cls): # Runs only once, setting up test data for all test methods
        # Create instances of objects for testing
        Order.objects.create(
            id=11,
            created_at='2021-01-01',
            vendor_id=22,
            customer_id=33
        )
        Order.objects.create(
            id=12,
            created_at='2021-01-01',
            vendor_id=22,
            customer_id=34
        )
        Order.objects.create(
            id=13,
            created_at='2021-01-02',
            vendor_id=24,
            customer_id=33
        )
        OrderLine.objects.create(
            order_id=11,
            product_id=41,
            product_description='RandomDescription',
            product_price=100,
            product_vat_rate=0.20,
            discount_rate=0.10,
            quantity=2,
            full_price_amount=200,
            discounted_amount=180,
            vat_amount=36,
            total_amount=144
        )
        OrderLine.objects.create(
            order_id=11,
            product_id=44,
            product_description='AnotherRandomDescription',
            product_price=120,
            product_vat_rate=0.20,
            discount_rate=0.10,
            quantity=1,
            full_price_amount=200,
            discounted_amount=180,
            vat_amount=36,
            total_amount=144
        )
        OrderLine.objects.create(
            order_id=12,
            product_id=41,
            product_description='RandomDescription',
            product_price=100,
            product_vat_rate=0.20,
            discount_rate=0.30,
            quantity=4,
            full_price_amount=200,
            discounted_amount=180,
            vat_amount=36,
            total_amount=144
        )
        OrderLine.objects.create(
            order_id=13,
            product_id=41,
            product_description='RandomDescription',
            product_price=100,
            product_vat_rate=0.20,
            discount_rate=0.10,
            quantity=4,
            full_price_amount=200,
            discounted_amount=180,
            vat_amount=36,
            total_amount=144
        )
        ProductPromotion.objects.create(
            date='2021-01-01',
            product_id=41,
            promotion_id=1
        )
        ProductPromotion.objects.create(
            date='2021-01-02',
            product_id=41,
            promotion_id=1
        )
        ProductPromotion.objects.create(
            date='2021-01-01',
            product_id=44,
            promotion_id=2
        )
        VendorCommissions.objects.create(
            date='2021-01-01',
            vendor_id=22,
            rate=0.10
        )
        VendorCommissions.objects.create(
            date='2021-01-02',
            vendor_id=22,
            rate=0.20
        )

    # Test logic for finding number of customers on a given day
    def test_number_of_customers(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Select distinct customer ids from orders
        distinct_customers = orders.values('customer_id').distinct()
        # Count distinct customer ids
        customers = distinct_customers.count()
        # Assert test
        self.assertEqual(customers, 2)

    # Test logic for finding total discount amount on a given day
    def test_total_discount_amount(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Set total discount amount variable
        total_discount_amount = 0
        # Loop through orders
        for order in orders:
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Loop through orderlines
            for orderline in orderlines:
                # Get discounted amount in each order line, and add to total_discount_amount
                if orderline.discount_rate != 0:  # discount_amount fields are not calculated correctly, so ignore if discount_rate is 0
                    total_discount_amount += orderline.discounted_amount
        # Assert test
        self.assertEqual(total_discount_amount, 540)

    # Test logic for finding the total number of items sold on a given day
    def test_items(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Set items variable
        items = 0
        # Loop through orders
        for order in orders:
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Loop through orderlines
            for orderline in orderlines:
                # Get quantity in each order line, and add to items
                items += orderline.quantity
        # Assert test
        self.assertEqual(items, 7)

    # Test logic for finding the average order total on a given day
    def test_order_total_avg(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Set order_total_sum variable
        order_total_sum = 0
        # Loop through orders
        for order in orders:
            # Set order total amount for each order
            single_order_total_amount = 0
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Loop through orderlines
            for orderline in orderlines:
                # Add order line total amount to the order's total amount
                single_order_total_amount += orderline.total_amount
            # Add the final order's total amount to the order total sum
            order_total_sum += single_order_total_amount
        # Calculate the order_total_avg value
        order_total_avg = order_total_sum / orders.count()
        # Assert test
        self.assertEqual(order_total_avg, 216)

    # Test logic for finding the averate discount rate applied to items on a given day
    def test_discount_rate_avg(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Set variable for the sum of all discount rates
        discount_rate_sum = 0
        # Set variable for the number of orderlines on a given day
        orderlines_sum = 0
        # Loop through orders
        for order in orders:
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Add orderlines in order to orderlines sum
            orderlines_sum += orderlines.count()
            # Loop through orderlines
            for orderline in orderlines:
                # Get discount rate, and add to discount rate sum
                discount_rate_sum += orderline.discount_rate
        # Calculate average discount rate across all orderlines
        discount_rate_avg_raw = discount_rate_sum / orderlines_sum
        discount_rate_avg = round(discount_rate_avg_raw, 2)
        # Assert test
        self.assertEqual(discount_rate_avg, 0.17)

    # Test logic to find the amount of commissions earned per promotion, on a given day
    def test_promo_commissions(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Create dictionary to store promotions and their commissions in
        promo_commissions = {}
        # Loop through orders
        for order in orders:
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Loop through orderlines
            for orderline in orderlines:
                # Check if there is a promotion for the product, on the given day
                product_promotion_qs = ProductPromotion.objects.filter(
                    Q(product_id=orderline.product_id) & Q(date='2021-01-01'))
                if product_promotion_qs:  # There is a promotion for the product
                    promotion_id = product_promotion_qs[0].promotion_id
                    # Add promotion to promo_commissions dict, if not already in dict
                    if not promo_commissions.get(promotion_id):
                        promo_commissions[promotion_id] = ''
                    # Find vendor commission rate, if valid for the date
                    vendorcommission_qs = VendorCommissions.objects.filter(
                        Q(vendor_id=order.vendor_id) & Q(date='2021-01-01'))
                    if vendorcommission_qs:
                        commission_rate = vendorcommission_qs[0].rate
                        commission_amount = orderline.total_amount * commission_rate
                        # Add commission to promo_commissions dict appropriately
                        if promo_commissions[promotion_id]:
                            promo_commissions[promotion_id] += commission_amount
                        else:
                            promo_commissions[promotion_id] = commission_amount
        # Create expected promo dict
        expected_dict = {1: 28.8, 2: 14.4}
        # Assert test
        self.assertEqual(promo_commissions, expected_dict)
    
    # Test logic to find the total amount of commissions on a given day
    def test_total_commissions(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Create variable for totalling commissions
        total_commissions = 0
        # Loop through orders
        for order in orders:
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Loop through orderlines
            for orderline in orderlines:
                # Find vendor commission rate
                vendorcommission_qs = VendorCommissions.objects.filter(
                    Q(vendor_id=order.vendor_id) & Q(date='2021-01-01'))
                if vendorcommission_qs:
                    commission_rate = vendorcommission_qs[0].rate
                    commission_amount = orderline.total_amount * commission_rate
                    # Add to total commissions
                    total_commissions += commission_amount
        # Assert test
        self.assertEqual(total_commissions, 43.2)

    # Test logic to find the average commission amount per order on a given day
    def test_order_avg_commission(self):
        # Get orders for date
        orders = Order.objects.filter(created_at__date='2021-01-01')
        # Create variable for totalling order commissions
        order_commissions_sum = 0
        # Loop through orders
        for order in orders:
            # Create variable for totalling each order's commissions
            order_commissions_total = 0
            # Get orderlines for order
            orderlines = OrderLine.objects.filter(order_id=order.id)
            # Loop through orderlines
            for orderline in orderlines:
                # Find vendor commission rate
                vendorcommission_qs = VendorCommissions.objects.filter(
                    Q(vendor_id=order.vendor_id) & Q(date='2021-01-01'))
                if vendorcommission_qs:
                    commission_rate = vendorcommission_qs[0].rate
                    commission_amount = orderline.total_amount * commission_rate
                    # Add to order's commissions total
                    order_commissions_total += commission_amount
            # Add order total commission to the sum of all order total commissions
            order_commissions_sum += order_commissions_total
        # Calculate order average commissions
        order_avg_commission = order_commissions_sum / orders.count()
        # Assert test
        self.assertEqual(order_avg_commission, 21.6)

        

