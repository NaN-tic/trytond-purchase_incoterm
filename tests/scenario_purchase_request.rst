=========================
Purchase Request Scenario
=========================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import (create_chart,
    ...     get_accounts, create_tax)

Install stock_supply and purchase_incoterm Module::

    >>> config = activate_modules(
    ...     ['purchase_request', 'stock_supply', 'purchase_incoterm'])

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> expense = accounts['expense']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Incoterm::

    >>> Incoterm = Model.get('incoterm')
    >>> incoterm, = Incoterm.find([], limit=1)

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()
    >>> supplier = Party(name='Supplier')
    >>> supplier.purchase_incoterm = incoterm
    >>> supplier.purchase_incoterm_place = 'Test Place'
    >>> supplier.save()

Create account category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.save()

    >>> account_category_tax, = account_category.duplicate()
    >>> account_category_tax.supplier_taxes.append(tax)
    >>> account_category_tax.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> ProductTemplate = Model.get('product.template')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])

    >>> template = ProductTemplate()
    >>> template.name = 'Product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal('20')
    >>> template.purchasable = True
    >>> template.account_category = account_category_tax
    >>> product, = template.products
    >>> product.cost_price = Decimal('8')
    >>> template.save()
    >>> product, = template.products

Get stock locations::

    >>> Location = Model.get('stock.location')
    >>> warehouse_loc, = Location.find([('code', '=', 'WH')])
    >>> supplier_loc, = Location.find([('code', '=', 'SUP')])
    >>> customer_loc, = Location.find([('code', '=', 'CUS')])
    >>> output_loc, = Location.find([('code', '=', 'OUT')])
    >>> storage_loc, = Location.find([('code', '=', 'STO')])

Create a need for missing product::

    >>> ShipmentOut = Model.get('stock.shipment.out')
    >>> shipment_out = ShipmentOut()
    >>> shipment_out.planned_date = datetime.date.today()
    >>> shipment_out.effective_date = datetime.date.today()
    >>> shipment_out.customer = customer
    >>> shipment_out.warehouse = warehouse_loc
    >>> shipment_out.company = company
    >>> move = shipment_out.outgoing_moves.new()
    >>> move.product = product
    >>> move.uom = unit
    >>> move.quantity = 1
    >>> move.from_location = output_loc
    >>> move.to_location = customer_loc
    >>> move.company = company
    >>> move.unit_price = Decimal('1')
    >>> move.currency = company.currency
    >>> shipment_out.click('wait')

There is no purchase request::

    >>> PurchaseRequest = Model.get('purchase.request')
    >>> PurchaseRequest.find([])
    []

Create the purchase request::

    >>> create_pr = Wizard('stock.supply')
    >>> create_pr.execute('create_')

There is now a draft purchase request::

    >>> pr, = PurchaseRequest.find([('state', '=', 'draft')])
    >>> pr.product == product
    True
    >>> pr.quantity
    1.0

Create the purchase then cancel it::

    >>> create_purchase = Wizard('purchase.request.create_purchase',
    ...     [pr])
    >>> create_purchase.form.party = supplier
    >>> create_purchase.execute('start')
    >>> pr.state
    'purchased'

    >>> Purchase = Model.get('purchase.purchase')
    >>> purchase, = Purchase.find()
    >>> purchase.incoterm == purchase.party.purchase_incoterm
    True
    >>> purchase.incoterm_place == purchase.party.purchase_incoterm_place
    True
