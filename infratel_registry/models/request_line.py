from odoo import models, fields, api


class RequestOpportunityLine(models.Model):
    _name = "crm.lead.line"

    code_deal = fields.Char(string="Codice tratta")
    route_length = fields.Char(string="Lunghezza tratta")
    product_service = fields.Many2one('product.template', string="Prodotto/Servizio")
    quantity = fields.Integer(string="Quantità")
    unit_of_measure = fields.Many2one('unit.measure', string="Unità di misura")
    #diameter = fields.Many2one('diameter.torque', string="Diametro/ Fibre cedute")
    duration_iru = fields.Many2one('iru.duration', string="Durata IRU")
    
    lead_id = fields.Many2one('crm.lead', string='Lead')