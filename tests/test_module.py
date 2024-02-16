
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from decimal import Decimal
from trytond.modules.company.tests import (
    CompanyTestMixin, create_company, set_company)
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.transaction import Transaction


class ProductPriceListPartyTestCase(CompanyTestMixin, ModuleTestCase):
    'Test ProductPriceListParty module'
    module = 'product_price_list_party'

    @with_transaction()
    def test_price_list(self):
        'Test price_list'
        pool = Pool()
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        Party = pool.get('party.party')
        Uom = pool.get('product.uom')
        PriceList = pool.get('product.price_list')

        company = create_company()
        with set_company(company):
            party1 = Party(name='Customer1')
            party1.save()
            party2 = Party(name='Customer1')
            party2.save()

            kilogram, = Uom.search([
                    ('name', '=', 'Kilogram'),
                    ])

            template = Template(
                name='Test Lot Sequence',
                list_price=Decimal(10),
                default_uom=kilogram,
                )
            template.save()
            product = Product(template=template)
            product.save()
            variant = Product(template=template)
            variant.save()

            price_list, = PriceList.create([{
                        'name': 'Default Price List',
                        'price': 'list_price',
                        'lines': [('create', [{
                                        'formula': 'unit_price * 0.8',
                                        'party': party1.id,
                                        }, {
                                        'formula': 'unit_price * 0.5',
                                        'party': party2.id,
                                        }, {
                                        'formula': 'unit_price',
                                        }])],
                        }])

            tests = [
                (variant, 1.0, kilogram, Decimal(8.0), party1),
                (variant, 1.0, kilogram, Decimal(5.0), party2),
                (variant, 1.0, kilogram, Decimal(10.0), None),

                ]
            for product, quantity, unit, result, party in tests:
                with Transaction().set_context(party=party and party.id):
                    self.assertEqual(
                        price_list.compute(product, quantity, unit),
                        result)

            # test with customer context
            with Transaction().set_context(customer=party1.id):
                self.assertEqual(
                    price_list.compute(variant, 1.0, kilogram),
                    Decimal(8.0))

del ModuleTestCase
