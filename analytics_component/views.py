from django.shortcuts import render, redirect
from .forms import DateForm
from .models import Order, OrderLine, ProductPromotion, VendorCommissions
from django.db.models import Q
import json

# Create your views here.

def index(request):
    """View to present the index page for the analytics_component app"""

    context = {}
    if request.method == 'POST':
        form = DateForm(data=request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            context['valid_date'] = date

            # Get orders for date
            orders = Order.objects.filter(created_at__date=date)

            if orders:
                # Select distinct customer ids from orders
                distinct_customers = orders.values('customer_id').distinct()
                # Count distinct customer ids
                customers = distinct_customers.count()

                # Create all required variables for analysis
                total_discount_amount = 0
                items = 0
                order_total_sum = 0
                orderlines_sum = 0
                discount_rate_sum = 0
                promo_commissions = {}
                total_commissions = 0
                order_commissions_sum = 0

                # Loop through orders
                for order in orders:
                    # Create all required variables for each order in the loop
                    single_order_total_amount = 0
                    order_commissions_total = 0

                    # Get orderlines for order
                    orderlines = OrderLine.objects.filter(order_id=order.id)

                    # Add count of orderlines to orderlines_sum
                    orderlines_sum += orderlines.count()

                    # Loop through orderlines
                    for orderline in orderlines:
                        # Get discounted amount in each order line, and add to total_discount_amount
                        if orderline.discount_rate != 0:  # discount_amount fields are not calculated correctly, so ignore if discount_rate is 0
                            total_discount_amount += orderline.discounted_amount

                        # Get quantity in each order line, and add to items
                        items += orderline.quantity

                        # Add order line total amount to the order's total amount
                        single_order_total_amount += orderline.total_amount

                        # Get discount rate, and add to discount rate sum
                        discount_rate_sum += orderline.discount_rate

                        # Total amount of commissions earned per promotion
                        # Check if there is a promotion for the product, on the given day
                        product_promotion_qs = ProductPromotion.objects.filter(
                            Q(product_id=orderline.product_id) & Q(date=date))
                        if product_promotion_qs:  # There is a promotion for the product
                            promotion_id = product_promotion_qs[0].promotion_id
                            # Add promotion to promo_commissions dict, if not already in dict
                            if not promo_commissions.get(promotion_id):
                                promo_commissions[promotion_id] = ''
                            # Find vendor commission rate, if valid for the date
                            vendorcommission_qs = VendorCommissions.objects.filter(
                                Q(vendor_id=order.vendor_id) & Q(date=date))
                            if vendorcommission_qs:
                                commission_rate = vendorcommission_qs[0].rate
                                commission_amount = orderline.total_amount * commission_rate
                                # Add commission to promo_commissions dict appropriately
                                if promo_commissions[promotion_id]:
                                    promo_commissions[promotion_id] += commission_amount
                                else:
                                    promo_commissions[promotion_id] = commission_amount

                        # Total and average amounts of commissions generated
                        # Find vendor commission rate, for given date
                        vendorcommission_qs = VendorCommissions.objects.filter(
                            Q(vendor_id=order.vendor_id) & Q(date=date))
                        # If the vendor has a commission set on this date
                        if vendorcommission_qs:
                            commission_rate = vendorcommission_qs[0].rate
                            commission_amount = orderline.total_amount * commission_rate
                            # Add to total commissions
                            total_commissions += commission_amount

                            # Add to order's commissions total
                            order_commissions_total += commission_amount

                    # Add the final order's total amount to the order total sum
                    order_total_sum += single_order_total_amount

                    # Add order total commission to the sum of all order total commissions
                    order_commissions_sum += order_commissions_total

                # Calculate the order_total_avg value
                order_total_avg = order_total_sum / orders.count()

                # Calculate average discount rate across all orderlines
                discount_rate_avg_raw = discount_rate_sum / orderlines_sum
                # Convert to 2dp
                discount_rate_avg = round(discount_rate_avg_raw, 2)

                # Calculate order average commissions
                order_avg_commission = order_commissions_sum / orders.count()

                json_tobe = {
                    'customers': customers,
                    'total_discount_amount': total_discount_amount,
                    'items': items,
                    'order_total_avg': order_total_avg,
                    'discount_rate_avg': discount_rate_avg,
                    'commissions': {
                        'promotions': promo_commissions,
                        'total': total_commissions,
                        'order_average': order_avg_commission
                    }
                }

                json_obj = json.dumps(json_tobe, indent = 4)
                context['json_obj'] = json_obj
            else:
                date_not_found = True
                context['date_not_found'] = date_not_found

    else:
        form = DateForm()

    context['form'] = form
    return render(request, 'analytics_component/index.html', context)
