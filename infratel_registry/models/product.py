from odoo import  models, fields

class ProductCustom(models.Model):
    _inherit = 'product.template'

    available_portal_side = fields.Boolean(string="Disponibile lato portale")
    diameter_torque = fields.Char(string="Diametro/Coppia")
