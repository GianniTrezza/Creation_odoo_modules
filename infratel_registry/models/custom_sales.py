from odoo import models, fields, api
from odoo.exceptions import UserError

class CustomSales(models.Model):
    _inherit = "sale.order"
    
    # Campo personalizzato project in custom_sale
    project_custom = fields.Many2one('project.request', string="Progetto reltivo a")
    order = fields.Char(string="Commessa")
    accordo_quadro = fields.Many2one('framework.agreements', string="Accordo quadro")
    cig = fields.Char(string="CIG")
    cup = fields.Char(string="CUP")
    request_type = fields.Selection([('backhauling', 'Backhauling'), ('rete_di_accesso', 'Rete di accesso')], string="Tipologi richiesta")
    refer = fields.Many2one('res.partner', string="Referenete")
    email_sales = fields.Char(string="Email",  compute="_compute_email_sales_custom")
    email_pec_sales = fields.Char(string="Email PEC", readonly ="True") #manca pec in contatti, devo inserire?
    phone_sales = fields.Char(string="Telefono", compute="_compute_phone_sales_custom")
    
    joint_tesing = fields.Boolean(string="Collaudo congiunto")
    maturity = fields.Date(string="Scadenza")
    
    # Temporaneo cosi ha detto Matteo siccome non ancora configurati
    business_developer = fields.Many2one('res.users', string="Business Developer")
    delivery_employee = fields.Many2one('res.users',  string="Dipendente delivery")
    
    quadrature_possible = fields.Boolean(string="Quadratura possibile")
    
    @api.depends('refer.email')
    def _compute_email_sales_custom(self):
        for record in self:
            if record.refer and record.refer.email:
                record.email_sales = record.refer.email
            else:
                record.email_sales = ""
                
    @api.depends('refer.email')
    def _compute_phone_sales_custom(self):
        for record in self:
            if record.refer and record.refer.phone:
                record.phone_sales = record.refer.phone
            else:
                record.phone_sales = ""
    
    def validation(self):
        return True
    def approval(self):
        return True
    def signature(self):
        return True
    def information(self):
        return True
    def purchase(self):
        return True
    def renewal(self):
        return True
    def divestment(self):
        return True  
# Generazione del wizard legato al tasto genera ODA
    def generate_purchase_order(self):
        self.ensure_one()
        if self.state != 'sale':
            raise UserError("L'ODV deve essere confermato per generare un ODA.")

        return {
            'name': 'Seleziona Fornitore',
            'type': 'ir.actions.act_window',
            'res_model': 'fornitori.wizard',  
            'view_mode': 'form',
            'target': 'new',
        }


class FornitoreWizard(models.TransientModel):
    _name = 'fornitori.wizard'
    _description = 'Selezione di un fornitore per l\'ODA'

    fornitore_id = fields.Many2one('res.partner', string='Fornitore', domain=[('type_contact', '=', 'fornitore')])
    # accordo_quadro_valido = fields.Boolean('Accordo Quadro Attivo', compute='_compute_accordo_quadro_valido')
    accordo_quadro_id = fields.Many2one('framework.agreements', string='Accordo Quadro', domain="[('associated_contract', '=', fornitore_id), ('is_state_valid', '=', True)]")
    # accordo_quadro_id = fields.Many2one('framework.agreements', string='Accordo Quadro', domain="[('associated_contract', '=', fornitore_id), ('state_bar_custom', '=', 'valid')]")

    
    def conferma_selezione_accordo_quadro(self):
        self.ensure_one()
        if not self.accordo_quadro_id:
            raise UserError('Seleziona un accordo quadro.')

        return {
            'name': 'Seleziona Prodotti',
            'type': 'ir.actions.act_window',
            'res_model': 'prodotti.lista',
            'view_mode': 'form',
            'target': 'new',
        }
    def conferma_selezione_fornitore(self):
        self.ensure_one()
        if not self.fornitore_id:
            raise UserError('Seleziona un fornitore.')
        if not self.fornitore_id.framework_agreement_count:
            raise UserError('Il fornitore selezionato non ha accordi quadro attivi.')

        return {
            'name': 'Seleziona Prodotti',
            'type': 'ir.actions.act_window',
            'res_model': 'prodotti.lista',
            'view_mode': 'form',
            'target': 'new',
        }
class ListaProdotti(models.TransientModel):
    _name = 'prodotti.lista'
    _description = 'Selezione dei prodotti per l\'ODA'

    product_ids = fields.Many2many('product.product', string='Prodotti')

    def conferma_selezione_prodotti(self):
        self.ensure_one()
        if not self.product_ids:
            raise UserError('Scegli almeno un prodotto.')



