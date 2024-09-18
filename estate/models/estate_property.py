from odoo import api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import *

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        (
            'check_positive_expected_price', 
            'CHECK(expected_price >= 0)',
            'Expected price must be positive'
        ),
        (
            'check-positive_selling_price',
            'CHECK(selling_price >= 0)',
            'Selling price must be positive' 
        )
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3), 
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        default='new'
    )
    type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one(
        'res.partner', 
        string = 'Buyer',
        copy = False
    )
    user_id = fields.Many2one(
        'res.users', 
        string = "Salesperson", 
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string = "Offers"
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = 0.00
            prices = prop.offer_ids
            if prices:
                prop.best_price = max(prices.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else ''
    
    def action_sold_property(self):
        for prop in self:
            if prop.state == 'canceled':
                raise UserError('Cannot set sold to canceled properties!')
            prop.state = 'sold'
        return True

    def action_cancel_property(self):
        for prop in self:
            if prop.state == 'sold':
                raise UserError('Cannot set canceled to sold properties!')
            prop.state = 'canceled'
        return True