# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond import backend
from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.pyson import Eval, Bool
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

purchase_incoterm = fields.Many2One('incoterm', 'Purchase Incoterm')
purchase_incoterm_place = fields.Char('Purchase Incoterm Name Place',
        states={
            'required': Bool(Eval('purchase_place_required')),
            'invisible': ~Bool(Eval('purchase_place_required')),
            },
        depends=['purchase_place_required'])


class Party(CompanyMultiValueMixin, metaclass=PoolMeta):
    __name__ = 'party.party'
    purchase_incoterm = fields.MultiValue(purchase_incoterm)
    purchase_incoterm_place = fields.MultiValue(purchase_incoterm_place)
    incoterms = fields.One2Many('party.party.incoterm', 'party', "Incoterms")
    purchase_place_required = fields.Function(fields.Boolean('Place Required'),
        'on_change_with_purchase_place_required')

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'purchase_incoterm', 'purchase_incoterm_place'}:
            return pool.get('party.party.incoterm')
        return super(Party, cls).multivalue_model(field)

    @fields.depends('purchase_incoterm')
    def on_change_with_purchase_place_required(self, name=None):
        if self.purchase_incoterm:
            return self.purchase_incoterm.purchase_place_required

    @fields.depends('purchase_incoterm', 'purchase_incoterm_place')
    def on_change_purchase_incoterm(self, name=None):
        self.purchase_incoterm_place = None


class PartyIncoterm(CompanyValueMixin, metaclass=PoolMeta):
    __name__ = 'party.party.incoterm'
    party = fields.Many2One(
        'party.party', "Party", ondelete='CASCADE', context={
            'company': Eval('company'),
        }, depends=['company'])
    purchase_incoterm = purchase_incoterm
    purchase_incoterm_place = fields.Char('Purchase Incoterm Name Place')

    @classmethod
    def __register__(cls, module_name):
        exist = backend.TableHandler.table_exist(cls._table)

        super(PartyIncoterm, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.extend(['purchase_incoterm', 'purchase_incoterm_place'])
        value_names.extend(['purchase_incoterm', 'purchase_incoterm_place'])
        migrate_property(
            'party.party', field_names, cls, value_names,
            parent='party', fields=fields)
