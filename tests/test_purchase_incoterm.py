# This file is part purchase_incoterm module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class PurchaseIncotermTestCase(ModuleTestCase):
    'Test Purchase Incoterm module'
    module = 'purchase_incoterm'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchaseIncotermTestCase))
    return suite
