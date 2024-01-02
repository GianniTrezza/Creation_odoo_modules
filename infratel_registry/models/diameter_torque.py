from odoo import models, fields

class diameter_torque(models.Model):
    _name = 'diameter.torque'

    id = fields.Integer(string="ID")
    name = fields.Char(string="Tipologia")
    size = fields.Char(string="Grandezza")
