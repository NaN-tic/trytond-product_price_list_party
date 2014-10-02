# This file is part of the product_price_list_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .price_list import *

def register():
    Pool.register(
        PriceList,
        PriceListLine,
        module='product_price_list_party', type_='model')
