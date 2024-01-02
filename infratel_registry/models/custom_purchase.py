from odoo import models, fields, api

class CustomSales(models.Model):
    _inherit = "purchase.order"
    
    project = fields.Many2one('project.request', string="Progetto relativo a ")
    order = fields.Char(string="Commessa")
    accordo_quadro = fields.Many2one('framework.agreements', string="Accordo quadro")
    cig = fields.Char(string="CIG")
    cup = fields.Char(string="CUP")
    request_type = fields.Selection([('backhauling', 'Backhauling'), ('rete_di_accesso', 'Rete di accesso')], string="Tipologia richiesta")
    refer = fields.Many2one('res.partner', string="Referenete")
    email_purchase_custom = fields.Char(string="Email", readonly="True", compute="_compute_email_purchase_custom")
    email_pec_purchase_custom = fields.Char(string="Email PEC", readonly="True") #manca email pac da inserire a contatti?
    phone_purchase_custom = fields.Char(string="Telefono", readonly="True", compute="_compute_phone_purchase_custom")
    sla_policy = fields.Many2one('sla.policy', string="Politica SLA")
    deadline = fields.Date(string="Deadline")
    actual_delivery_date = fields.Date(string="Data di consegna effettiva")
    delivery_employee = fields.Many2one('res.users',  string="Dipendente delivery")
    works_director = fields.Many2one('res.partner', string="Direttore  lavori")
    execution_security_coordinator = fields.Many2one('res.partner', string="Coordinatore sicurezza esecuzione")
    design_safety_coordinator = fields.Many2one('res.partner', string="Coordinatore sicurezza progettazione")
    joint_tesing = fields.Boolean(string="Collaudo congiunto")
    maturity = fields.Date(string="Scadenza")
    
    @api.depends('refer.email')
    def _compute_email_purchase_custom(self):
        for record in self:
            if record.refer and record.refer.email:
                record.email_purchase_custom = record.refer.email
            else:
                record.email_purchase_custom = ""
                
    @api.depends('refer.email')
    def _compute_phone_purchase_custom(self):
        for record in self:
            if record.refer and record.refer.phone:
                record.phone_purchase_custom = record.refer.phone
            else:
                record.phone_purchase_custom = ""
                
    def validation(self):
        return True
    def approval(self):
        return True
    def signature(self):
        return True
    def information(self):
        return True
    def suspend(self):
        return True
    def reactivate(self):
        return True
    def new_order(self):
        return True
    