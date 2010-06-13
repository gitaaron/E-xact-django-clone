from django.db import models
from django.contrib import admin

from exact_clone.shop.utils import round_decimal

# Create your models here.
CART_ID = 'cartID'

class Product(models.Model):
    photo = models.OneToOneField('gallery.Photo')
    price = models.DecimalField(null=False, blank=False, max_digits=18,decimal_places=10)
    def __unicode__(self):
        return u'%s : $%s' % (self.photo.title, round_decimal(self.price, 2)) 


class CartItemManager(models.Manager):
    def from_request(self, request):
        '''
        Get the current cart from the request.
        If none exists then create it.
        '''
        cart_id = request.session.get(CART_ID, False)
        cart = None
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                del(request.session[CART_ID])

        if not cart:
            cart = Cart()
            cart.save()
            request.session[CART_ID] = cart.id

        return cart

class CartItem(models.Model):
    product = models.ForeignKey('Product')
    cart = models.ForeignKey('Cart')
    quantity = models.DecimalField(max_digits=18, decimal_places=6,default=0)

    def _line_item_total(self):
        return round_decimal(float(self.product.price) * float(self.quantity), 2)
    line_item_total = property(_line_item_total)



class Cart(models.Model):
    date_time_created = models.DateTimeField(auto_now_add=True)

    objects = CartItemManager()

    def _is_empty(self):
        return self.cartitem_set.count()==0
    is_empty = property(_is_empty)

    def remove_all_items(self):
        items = self.cartitem_set.all()
        for item in items:
            item.delete()

    def add_item(self, chosen_item, number_added):
        # see if item for this product already exists
        try:
            item = CartItem.objects.get(product=chosen_item, cart=self)
        except CartItem.DoesNotExist:
            item = CartItem(cart=self,product=chosen_item)
            
        item.quantity += int(number_added)
        item.save()

        return item

    def _sub_total(self):
        items = self.cartitem_set.all()
        sub_total = 0
        for item in items:
            sub_total += item.product.price * item.quantity

        return round_decimal(sub_total, 2)
    sub_total = property(fget=_sub_total)

    def _num_items(self):
        items = self.cartitem_set.all()
        q = 0
        for item in items:
            q += item.quantity

        return q
    num_items = property(fget=_num_items)

    def _tax_amount(self):
        '''
        Assume 15% taxes to make things simple.
        '''
        return round_decimal(float(self.sub_total) * 0.15, 2)
    tax_amount = property(fget=_tax_amount)

    def _total(self):
        return round_decimal(float(self.sub_total) + float(self.tax_amount), 2)
    total = property(fget=_total)

    def _shipping(self):
        '''
        Assume shipping always costs $15 for simplicity.
        '''
        return 15
    shipping = property(fget=_shipping)

    def clear(self):
        pass


admin.site.register(Product)
