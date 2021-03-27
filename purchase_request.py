# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class PurchaseRequest(metaclass=PoolMeta):
    __name__ = 'purchase.request'
    incoterm = fields.Function(fields.Many2One('incoterm', 'Incoterm'),
        'get_incoterm')
    incoterm_place = fields.Function(fields.Char('Incoterm Place'),
        'get_incoterm')

    @classmethod
    def get_incoterm(cls, requests, names):
        res = {n: {r.id: None for r in requests} for n in names}
        for name in names:
            for req in requests:
                if req.party:
                    if name == 'incoterm' and req.party.purchase_incoterm:
                        res[name][req.id] = req.party.purchase_incoterm.id
                    elif (name == 'incoterm_place'
                            and req.party.purchase_incoterm_place):
                        res[name][req.id] = req.party.purchase_incoterm_place
        return res


class CreatePurchase(metaclass=PoolMeta):
    __name__ = 'purchase.request.create_purchase'

    @classmethod
    def _group_purchase_key(cls, requests, request):
        key = super(CreatePurchase, cls)._group_purchase_key(requests, request)
        return key + (
            ('incoterm', request.incoterm),
            ('incoterm_place', request.incoterm_place),
            )
