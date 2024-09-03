from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import *

class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        (
            'check_positive_price',
            'CHECK(price >= 0)',
            'Offer price must be positive'
        )
    ]
    
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner", 
        string="Buyer", 
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string = "Property",
        required = True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline")

    @api.depends('validity','create_date')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        self.write({
            "status": "accepted"
        })
        for offer in self:
            offer.property_id.state = 'offer_accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True

    @api.constrains('price', 'property_id.expected_price')
    def check_selling_price(self):
        for prop in self:
            if prop.price < (prop.property_id.expected_price * 0.9):
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")