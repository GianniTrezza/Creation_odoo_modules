from odoo import models, fields, api


class IruDuration(models.Model):
    _name = "iru.duration"
    
    name = fields.Char(string="Tipologia")