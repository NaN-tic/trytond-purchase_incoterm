# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import incoterm
from . import party
from . import purchase


def register():
    Pool.register(
        incoterm.Incoterm,
        party.Party,
        party.PartyIncoterm,
        purchase.purchase,
        module='purchase_incoterm', type_='model')
