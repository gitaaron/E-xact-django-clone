'''
Taken from the satchmo project.
'''
from decimal import Decimal, ROUND_DOWN, InvalidOperation, getcontext

def round_decimal(val='0', places=None, roundfactor='0', normalize=False):
    """
    PARTIAL UNIT ROUNDING DECIMAL
    Converts a valid float, integer, or string to a decimal number with a specified
    number of decimal places, performs "partial unit rounding", and decimal normalization.

    METHOD ARGUEMENTS:
    `val` The value to be converted and optionally formated to decimal.
    `places` The decimal precision is defined by integer "places" and
        must be <= the precision defined in the decimal.Decimal context.
    `roundfactor` (partial unit rounding factor) If purf is between -1 and 1, purf rounds up
        (positive purf value) or down (negative purf value) in factional "purf" increments.
    `normalize` If normalize is True (any value other than False), then rightmost zeros are truncated.
    """

    #-- Edit function arguments and set necessary defaults

    if str(normalize) == 'False': normalize = False     #Allow templates to submit False from filter

    try:
        roundfactor = Decimal(str(roundfactor))
    except (InvalidOperation, ValueError):
        raise RoundedDecimalError(val=roundfactor, id =1, msg="roundfactor - InvalidOperation or ValueError")  #reraise exception and return to caller
    if not (abs(roundfactor) >= 0 and abs(roundfactor) <= 1):
        raise RoundedDecimalError(val=roundfactor, id=2, msg="roundfactor - Out of Range - must be between -1 and +1")
    try:
        if places != None: places = int(places)
    except ValueError:
        raise RoundedDecimalError(val=places, id=3, msg='ValueError, Invalid Integer ')
    if places > getcontext().prec:
        raise RoundedDecimalError(val=places, id=4, msg='places Exceeds Decimal Context Precision')
    try:
        decval =Decimal(str(val))
    except (InvalidOperation, UnicodeEncodeError):
        raise RoundedDecimalError(val=val, id=5, msg='InvalidOperation - val cannot be converted to Decimal')

    #-- Round decimal number by the Partial Unit Rounding Factor
    if roundfactor and decval%roundfactor:
        if roundfactor < 0: roundby = 0
        else: roundby = (decval/abs(decval))*roundfactor	#change sign of roudby to decval
        decval=(decval//roundfactor*roundfactor)+roundby #round up or down by next roundfactor increment

    #-- Adjust number of decimal places if caller provided decimal places
    if places != None:
        decmask = '0.'.ljust(places+2,'0') #i.e. => '.00' if places eq 2
        decval=decval.quantize(Decimal(decmask), rounding=ROUND_DOWN)  #convert to Decimal and truncate to two decimals

    #-- normalize - strips the rightmost zeros... i.e. 2.0 => returns as 2
    if normalize:
        # if the number has no decimal portion return just the number with no decimal places
        # if the number has decimal places (i.e. 3.20), normalize the number (to 3.2)
        # This check is necesary because normalizing a number which trails in zeros (i.e. 200 or 200.00) normalizes to
        # scientific notation (2E+2)
        if decval==decval.to_integral():
            decval = decval.quantize(Decimal('1'))
        else:
            decval.normalize()

    return decval

class RoundedDecimalError:
    """
     General Purpose Error Handling used to handle error exceptions
     created in caller.
     Caller name and module taken from
     Activestate Recipe 66062: Determining Current Function Name
        # sys._getframe().f_code.co_name
        # sys._getframe().f_lineno
        # sys._getframe().f_code.co_filename
    """

    def __repr__(self):
        return "RoundedDecimalError - Partial Unit Rounding Error Exception Occured"

    def __init__(self, val='', id='', msg=''):
        import sys
        self.val = val
        self.id = id
        self.msg = msg
        self.caller_name = sys._getframe(1).f_code.co_name		#callers name
        self.caller_module = sys._getframe(1).f_code.co_filename	#module name of caller
        self.caller_lineno = sys._getframe(1).f_lineno		#line number of caller



def get_filter_args(argstring, keywords=(), intargs=(), boolargs=(), stripquotes=False):
    """
    Converts a string formatted list of arguments into a kwargs dictionary.
    Automatically converts all keywords in intargs to integers.

    If keywords is not empty, then enforces that only those keywords are returned.
    Also handles args, which are just elements without an equal sign

    ex:
    in: get_filter_args('length=10,format=medium', ('length'))
    out: (), {'length': 10, 'format':'medium'}
    """
    args = []
    kwargs = {}
    if argstring:
        work = [x.strip() for x in argstring.split(',')]
        work = [x for x in work if x != '']
        for elt in work:
            parts = elt.split('-',1)
            if len(parts)==1:
                if stripquotes:
                    elt=_stripquotes(elt)
                args.append(elt)
            else:
                key, val = parts
                val = val.strip()
                if stripquotes and val:
                    val=_stripquotes(val)

                key = key.strip()
                if not key:continue
                key = key.lower().encode('ascii')

                if not keywords or key in keywords:
                    if key in intargs:
                        try:
                            val = int(val)
                        except ValueError:
                            raise ValueError('Could not convert value "%s" to integer for keyword "%s"' % (val,key))
                    if key in boolargs:
                        val = val.lower()
                        val = val in (1,'t','true','yes','y','on')
                    kwargs[key] = val

    return args, kwargs

def _stripquotes(val):
    stripping = True
    while stripping:
        stripping = False
        if val[0] in ('"', "'"):
            val = val[1:]
            stripping = True
        if val[-1] in ('"', "'"):
            val = val[:-1]
            stripping = True

    return val

