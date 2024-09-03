from odoo import fields, models

class Type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        (
            'unique_type',
            'UNIQUE(name)',
            'Type name must be unique'
        )
    ]

    name = fields.Char(required=True)