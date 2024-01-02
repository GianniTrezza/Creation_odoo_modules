from datetime import date
from odoo import models, api, fields

class FrameworkAgreements(models.Model):
    _name = 'framework.agreements'

    name = fields.Char(string="Nome contratto")
 
    associated_contract = fields.Many2one('res.partner', string="Contatto associato")
    type_contract = fields.Char(string="Tipo contatto", readonly="True", compute="_compute_type_contract")
    start_date = fields.Date(string="Data di inizio")
    end_date = fields.Date(string="Valido fino a")
    contract = fields.Binary(string="Contratto")
    day_allert = fields.Integer(string="Giorni allert")
    sla_policy = fields.Many2one('sla.policy', string="Politiche SLA")
    infratel_protocol = fields.Char(string="Protocollo Infratel")
    signing_date = fields.Date(string="Data di sottoscrizione")
    date_today = fields.Date(string='Data odierna', default=fields.Date.context_today)
    cig = fields.Char(string="CIG")
    state_bar_custom = fields.Selection([('valid', 'Valido'), ('not_valid', 'Non valido')],
                             string="Stato",
                             default='not_valid',
                             compute="_compute_state"
                             )
    
    is_state_valid = fields.Boolean(
        string="Stato Validità",
        compute="_compute_is_state_valid",
        store=True
    )
    
    products_lines = fields.One2many('tab.request', 'request_id', string='Prodotti abilitati')
    
    
    def _compute_state(self):
        for record in self:
            today = date.today()
            if record.start_date and record.start_date > today:
                record.state_bar_custom = 'not_valid'
            elif record.end_date and record.end_date < today:
                record.state_bar_custom = 'not_valid'
            else:
                record.state_bar_custom = 'valid'
    
    @api.depends('associated_contract')
    def _compute_type_contract(self):
        for record in self:
            if record.associated_contract:
                record.type_contract = record.associated_contract.type_contact
            else:
                record.type_contract = False

    @api.depends('state_bar_custom')
    def _compute_is_state_valid(self):
        for record in self:
            record.is_state_valid = (record.state_bar_custom == 'valid')
    
    
    # state_bar_custom_search = fields.Selection(
    #     [('valid', 'Valido'), ('not_valid', 'Non valido')],
    #     string="Stato per la ricerca",
    #     compute="_compute_state_bar_custom_search",
    #     search="_search_state_bar_custom"
    # )
    
    
    
    # @api.depends('state_bar_custom')
    # def _compute_state_bar_custom_search(self):
    #     for record in self:
    #         record.state_bar_custom_search = record.state_bar_custom

    # def _search_state_bar_custom(self, operator, value):
    #     return [('state_bar_custom', operator, value)]
    
    
    
    
    
    
    
                