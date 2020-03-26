import json

from decimal import Decimal

# ----------------------------------------------------------------
def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError
# ----------------------------------------------------------------
aa = ['string', Decimal(3.4), Decimal(5.3)]
json_str = json.dumps(aa, default=decimal_default_proc)
print('aa:', aa)
print('json_str:', json_str)
# ----------------------------------------------------------------