from odoo import models, fields

class StrutturaSanitaria(models.Model):
    _inherit = 'res.partner'

    is_struttura_sanitaria = fields.Boolean('È una struttura sanitaria')
    e_accreditata = fields.Boolean('Accreditata')