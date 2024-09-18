from odoo import fields, models

class Type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        (
            'unique_type',
            'UNIQUE(name)',
            'Type name must be unique'
        )
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'type_id',
        string="Properties"
    )
    sequence = fields.Integer()