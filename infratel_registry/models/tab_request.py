from odoo import models, fields, api

class tabRequest(models.Model):
    _name = 'tab.request'
    
    product_request = fields.Many2one('product.template', string="Prodotti")
    price_request = fields.Float(string="Prezzo", compute="_compute_price_unit", readonly=False,)
    
    request_id = fields.Many2one('framework.agreements', string='Richiesta prodotto')
    
    @api.depends('product_request')
    def _compute_price_unit(self):
        for request in self:
            if request.product_request:
                request.price_request = request.product_request.list_price