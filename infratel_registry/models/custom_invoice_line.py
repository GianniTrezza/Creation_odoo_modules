from odoo import models, fields, api


class CustomInvoicesLine(models.Model):
    _inherit = "account.move.line"
    
    tratta  = fields.Many2one('plant.routes', string="Tratta")
    code_deal = fields.Char(string="Codice tratta")
    route_length = fields.Char(string="Lunghezza tratta")
    product_service = fields.Many2one('product.template', string="Prodotto/Servizio")
    #quantity = fields.Integer(string="Quantità") Già  è base
    unit_of_measure = fields.Many2one('unit.measure', string="Unità di misura")
    diameter = fields.Many2one('diameter.torque', string="Diametro/ Fibre cedute")
    #unit_prince = fields.Integer(string="Prezzo unitario") Gia è base
    #taxes = fields.Many2one('account.tax') Già è base
    #prezzo totale  gia è base
    good_receipt = fields.Boolean(string="Entrata merci registrata")
    good_receipt_code = fields.Char(string="Codice entrata merci")
    good_receipt_validity = fields.Date(string="Validità  entrata merci") 