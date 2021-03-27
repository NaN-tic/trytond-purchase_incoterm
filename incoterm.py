# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Incoterm(metaclass=PoolMeta):
    __name__ = 'incoterm'

    purchase_place_required = fields.Boolean('Purchase place required',
        help="Make place required for this incoterm (purchase)")

    @staticmethod
    def default_purchase_place_required():
        return False
