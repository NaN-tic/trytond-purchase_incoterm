# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import incoterm
from . import party
from . import purchase
from . import purchase_request

def register():
    Pool.register(
        incoterm.Incoterm,
        party.Party,
        party.PartyIncoterm,
        purchase.Purchase,
        module='purchase_incoterm', type_='model')
    Pool.register(
        purchase_request.PurchaseRequest,
        depends=['purchase_request'],
        module='purchase_incoterm', type_='model')
    Pool.register(
        purchase_request.CreatePurchase,
        depends=['purchase_request'],
        module='purchase_incoterm', type_='wizard')
