# This file is part of the product_price_list_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PriceList', 'PriceListLine']


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'

    def compute(self, party, product, unit_price, quantity, uom,
            pattern=None):
        if pattern is None:
            pattern = {}
        if party:
            pattern['party'] = party.id
        return super(PriceList, self).compute(party, product, unit_price,
            quantity, uom, pattern)


class PriceListLine(metaclass=PoolMeta):
    __name__ = 'product.price_list.line'
    party = fields.Many2One('party.party', 'Party')
