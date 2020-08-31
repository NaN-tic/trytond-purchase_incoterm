# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['Purchase']


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'
    incoterm = fields.Many2One('incoterm', 'Incoterm',
        states={
            'readonly': Eval('state').in_(['processing', 'cancelled', 'done']),
            },
        depends=['state'])
    incoterm_place = fields.Char('Incoterm Name Place',
        states={
            'required': Bool(Eval('incoterm')),
            'invisible': ~Bool(Eval('incoterm')),
            'readonly': Eval('state').in_(['processing', 'cancelled', 'done']),
            },
        depends=['state', 'incoterm'])

    def on_change_party(self):
        super(Purchase, self).on_change_party()

        self.incoterm = None
        self.incoterm_place = None
        if self.party:
            self.incoterm = self.party.purchase_incoterm \
                if self.party.purchase_incoterm else None
            self.incoterm_place = self.party.purchase_incoterm_place \
                if self.party.purchase_incoterm_place else None
