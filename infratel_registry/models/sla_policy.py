from odoo import fields, models

class sla_policy(models.Model):
    _name = "sla.policy"
    _rec_name = "type_policy"

    type_policy = fields.Char(string="Tipo politica")
    description = fields.Char(string="Descrizione")
    labels = fields.Many2one('sla.policy',  string="Etichette")
    timing = fields.Integer(string="Tempistica")
    unit = fields.Selection([('day', 'giorno'),('month', 'mese'),('year', 'anno')], string="Unità di misura")
