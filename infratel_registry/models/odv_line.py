from odoo import models, fields, api


class OdVLine(models.Model):
    _inherit = "sale.order.line"

    tratta  = fields.Many2one('plant.routes', string="Tratta")
    code_deal = fields.Char(string="Codice tratta")
    route_length = fields.Char(string="Lunghezza tratta")
    product_service = fields.Many2one('product.template', string="Prodotto/Servizio")
    #quantity = fields.Integer(string="Quantità") Già  è base
    unit_of_measure = fields.Many2one('unit.measure', string="Unità di misura")
    diameter = fields.Many2one('diameter.torque', string="Diametro/ Fibre cedute")
    
    