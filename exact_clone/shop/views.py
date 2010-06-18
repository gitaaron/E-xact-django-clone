import time
from decimal import Decimal

from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.core import urlresolvers
from django.conf import settings

from exact_clone.shop.models import Cart, Product, Order

def display_cart(request):
    return direct_to_template(request, 'shop/cart.html', {'payment_settings':_get_payment_settings()})

def payment_notification(request):
    '''
    Validate the order.
    Create an order from the cart.
    Clear the cart and redirect to a success page.
    '''
    # @TODO validation code will go here

    cart = Cart.objects.from_request(request)
    order = Order.objects.from_cart(cart)
    cart.remove_all_items()
    return HttpResponseRedirect(urlresolvers.reverse('exact_clone.shop.views.display_order', args=[order.id,]))


def display_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404()

    return direct_to_template(request, 'shop/checkout_success.html', {'order':order})


def empty_cart(request):
    cart = Cart.objects.from_request(request)
    cart.remove_all_items()
    return HttpResponseRedirect(urlresolvers.reverse('exact_clone.shop.views.display_cart'))

def add_item(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    product_id = request.POST.get('product')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404()

    quantity = request.POST.get('quantity')

    cart = Cart.objects.from_request(request)
    cart.add_item(product, quantity)

    return HttpResponseRedirect(urlresolvers.reverse('exact_clone.shop.views.display_cart'))


import hmac
import hashlib
from exact_clone.shop.utils import round_decimal

def _get_payment_settings():
    payment_settings = settings.PAYMENT_PAGE_VARS
    payment_settings['x_fp_timestamp'] = round_decimal(time.time(), 0)
    payment_settings['x_amount'] = round_decimal(34.23, 2)
    payment_settings['x_fp_hash'] = _get_hash(payment_settings)
    payment_settings['x_fp_hash_str'] = _get_hash_string(payment_settings)
    return payment_settings

def _get_hash_string(payment_settings):
    # %(x_login)^%(x_fp_sequence)^%(x_fp_timestamp)^%(x_amount)^%(x_currency)

    data =  '%(x_login)s^%(x_fp_sequence)s^%(x_fp_timestamp)s^%(x_amount)s^%(x_currency)s' \
             %  {'x_login': payment_settings['x_login'], 'x_fp_sequence' : payment_settings['x_fp_sequence'],\
             'x_fp_timestamp' : payment_settings['x_fp_timestamp'], 'x_amount' : payment_settings['x_amount'], 'x_currency' : ''}

    return data

def _get_hash(payment_settings):
    # Instantiate hmac with Transaction key (HMAC-MD5)
    digest_maker = hmac.new(settings.PAYMENT_TRANSACTION_KEY, '', hashlib.md5) # NOTE: by default the payment page is set up to use md5, change this to sha1 if you generated your keys that way
    data = _get_hash_string(payment_settings)
    digest_maker.update(data)
    x_fp_hash = digest_maker.hexdigest()
    return x_fp_hash

