from odoo import models, fields, api


class RequestOpportunity(models.Model):
    _inherit = "crm.lead"

    region = fields.Char(string="Regione")
    birthplace = fields.Char(string="Comune")
    project = fields.Many2one('project.request', string="Progetto relativo a")
    shop_assistant = fields.Char(string="Commessa")
    #framework_agreement_crm = fields.Char(string="Accordo Quadro (da fare select)")
    cig = fields.Char(string="CIG")
    cup = fields.Char(string="CUP")
    type_request = fields.Selection([('backhualing', 'Backhualing'), ('access_network', 'Rete di accesso')], string="Tipo richiesta")
    pec = fields.Char(string="E-mail PEC")
    joint_testing = fields.Boolean(string="Collaudo congiunto")
    referent_cust = fields.Many2one('res.partner', string="Referente", domain="[('type_contact','=','operatore')]")
    date_today = fields.Date(string='Data odierna', default=fields.Date.context_today)
    associated_framework_agreements = fields.Many2one(
                                                    'framework.agreements',
                                                    string="Accordo quadro associato",
                                                    #domain="[('is_state_valid', '=', True)]"
                                                    )                                                   
     
    

   
    opportunity_lines = fields.One2many('crm.lead.line', 'lead_id', string='CRM Lines')
    
    
    