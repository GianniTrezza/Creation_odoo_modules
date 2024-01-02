from odoo import fields, models

class project_request(models.Model):
    _name = "project.request"

    
    name = fields.Char(string="Nome progetto")
    description = fields.Char(string="Descrizione progetto")
    
    partner_id = fields.Many2one('res.partner', string="Cliente Associato")