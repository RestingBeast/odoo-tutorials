from odoo import fields, models

class Tag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        (
            'unique_tag',
            'UNIQUE(name)',
            'Tag name must be unique'
        )
    ]

    name = fields.Char(required=True)