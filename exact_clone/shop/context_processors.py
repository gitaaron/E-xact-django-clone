from exact_clone.shop.models import Cart

def cart(request):
    return {'cart':Cart.objects.from_request(request)}
