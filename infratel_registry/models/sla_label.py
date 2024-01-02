from odoo import models, fields, api

class SlaLabel(models.Model):
    _name = 'sla.label'
    
    name = fields.Char(string="Nome Etichetta")
    