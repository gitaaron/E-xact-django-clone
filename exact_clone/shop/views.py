from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.core import urlresolvers

from exact_clone.shop.models import Cart, Product

def display_cart(request):
    return direct_to_template(request, 'cart.html')

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

def checkout(request):
    return HttpResponse('ok')


def empty_cart(request):
    cart = Cart.objects.from_request(request)
    cart.remove_all_items()
    return HttpResponseRedirect(urlresolvers.reverse('exact_clone.shop.views.display_cart'))
