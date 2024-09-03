from odoo import api, fields, models
from dateutil.relativedelta import *

class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

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
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True