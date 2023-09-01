# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class TipologiaPratica(models.Model):
    _name = 'hospital.tipologia_pratica'
    _description = 'Type of Accreditation Practice'

    name = fields.Char(string='Nome', required=True)





