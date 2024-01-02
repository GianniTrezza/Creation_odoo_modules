
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    type_contact = fields.Selection([('operatore', 'Operatore'), ('fornitore', 'Fornitore')], string="Tipo contatto")
    enabled = fields.Boolean(string="Abilitato")
    active_framework_agreement = fields.Boolean(string="Accordo quadro attivo")
    
    framework_agreement_list = fields.One2many("framework.agreements", "associated_contract", string="Accordo quadro Lista")
    framework_agreement_count = fields.Integer("Framework Count", compute="_framework_agreement_count")
    
    
    @api.depends("framework_agreement_list")
    def _framework_agreement_count(self):
        for rec in self:
            rec.framework_agreement_count = len(rec.framework_agreement_list)

    def smartButton(self):
        return {
            "name": "Accordi Quadro",
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "views": [(False, 'tree'), (False, 'form')],
            'res_model': "framework.agreements",
            'domain': [('associated_contract', '=', self.id)],
            'context': {'default_associated_contract': self.id},
        }