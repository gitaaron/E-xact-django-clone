from django import template
from django.utils.safestring import mark_safe
from exact_clone.shop.utils import get_filter_args
from exact_clone.shop.utils import round_decimal, RoundedDecimalError

register = template.Library()

def normalize_decimal(value, args=""):
    '''
    A template_tag wrapper to round_decimal.

    Usage:
    val|normalize_decimal
    val|normalize_decimal:'places=2'
    val|normalize_decimal:'places=2:roundfactor=.5'
    val|normalize_decimal:'places=2:roundfactor=.5:normalize=False'

    '''
    if value == '' or value is None:
        return value
    args, kwargs = get_filter_args(args,
            keywords=('places','roundfactor','normalize'),
            intargs=('places',),
            boolargs=('normalize',), stripquotes=True)

    if not 'places' in kwargs:
        kwargs['places'] = 2

    print 'val : %s' % round_decimal(val=value, **kwargs)
    try:
        return mark_safe(str(round_decimal(val=value, **kwargs)))
    
    except RoundedDecimalError, e:
        return value

register.filter('normalize_decimal', normalize_decimal)
normalize_decimal.is_safe = True
