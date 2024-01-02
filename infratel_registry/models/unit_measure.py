from odoo import models, fields


class drawn(models.Model):
    _name = "unit.measure"
    
    unit_of_measure = fields.Char(string="Unità di msiura (simbolo)")
    extended_unit_of_measure =  fields.Char(string="Unità di misura ")
    