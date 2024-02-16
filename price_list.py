# This file is part of the product_price_list_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'

    def compute(self, product, quantity, uom, pattern=None):
        context = Transaction().context

        if pattern is None:
            pattern = {}
        # sale module add customer in search_context product
        pattern['party'] = context.get('customer') or context.get('party')
        return super().compute(product, quantity, uom, pattern)


class PriceListLine(metaclass=PoolMeta):
    __name__ = 'product.price_list.line'
    party = fields.Many2One('party.party', 'Party')
