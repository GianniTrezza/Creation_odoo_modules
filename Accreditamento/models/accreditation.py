from odoo import models, api, fields, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = "res.partner"
    is_accreditata = fields.Boolean(string='Accreditata')
    is_struttura_sanitaria = fields.Boolean(string='Struttura Sanitaria', default=False)


class HospitalAccreditation(models.Model):
    _name = 'hospital.accreditation'
    _description = 'Accreditation of Healthcare Structures'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_user(self):
        return self.env.user.id

    codice_pratica = fields.Char(string='Codice Pratica', readonly=True, copy=False, default=lambda self: _('New'))
    autore_registrazione = fields.Many2one('res.users', string='Autore Registrazione', default=_get_default_user, readonly=True)
    tipologia_pratica_id = fields.Many2one('hospital.tipologia_pratica', string='Tipologia Pratica', required=True)
    richiedente_id = fields.Many2one('res.partner', string='Richiedente', domain=[('is_company', '=', False)])
    struttura_da_accreditare_id = fields.Many2one('res.partner', string='Struttura da Accreditare', domain=[('is_company', '=', True), ('is_struttura_sanitaria', '=', True)], required=True)
    descrizione = fields.Html(string='Descrizione')
    state = fields.Selection([
        ('recorded', 'In compilazione'),
        ('to_be_approved', 'Da approvare'),
        ('approved', 'Approvato'),
        ('refused', 'Rifiutato'),
        ('reverted', 'Inverti Stato'),
    ], string='Stato', default='recorded', readonly=True, track_visibility='onchange')
    
    @api.model
    def create(self, vals):
        if not vals.get('codice_pratica'):
            sequence_value = self.env['ir.sequence'].next_by_code('hospital.accreditation.sequence') or _('New')
            vals['codice_pratica'] = sequence_value
        return super(HospitalAccreditation, self).create(vals)

    def write(self, vals):
        for record in self:
            if record.state in ['approved', 'refused', 'reverted'] and not record.codice_pratica:
                sequence_value = self.env['ir.sequence'].next_by_code('hospital.accreditation.sequence') or _('New')
                vals['codice_pratica'] = sequence_value
        return super(HospitalAccreditation, self).write(vals)

    def button_recorded(self):
        for record in self:
            record.state = "recorded"
        return True
    
    def button_to_be_approved(self):
        return {
            'name': _('Decide on Accreditation'),
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.accreditation.decision.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id}
        }

    def button_approve(self):
        for record in self:
            record.state = 'approved'
            record.struttura_da_accreditare_id.is_accreditata = False
        return {
                'type': 'ir.actions.act_window',
                'name': 'Pratiche',
                'res_model': 'hospital.accreditation',
                'view_mode': 'tree,form',
                'target': 'current',
        }

    def button_refuse(self):
        for record in self:
            record.state = 'refused'
            record.struttura_da_accreditare_id.is_accreditata = False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pratiche',
            'res_model': 'hospital.accreditation',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    # def button_revert_refusal(self):
    #     for record in self:
    #         if record.state in ['refused', 'approved']:
    #             record.state = 'to_be_approved'
    #     return True
    def button_revert_refusal(self):
        for record in self:
            if record.state == 'refused':
                record.state = 'approved'
            elif record.state == 'approved':
                record.state = 'refused'
        return True




class HospitalAccreditationDecisionWizard(models.TransientModel):
    _name = "hospital.accreditation.decision.wizard"
    _description = "Decide on Hospital Accreditation"

    decision = fields.Selection([
        ('approved', 'Approva'),
        ('refused', 'Rifiuta'),
    ], string='Decision', required=True)

    def action_confirm(self):
        active_id = self.env.context.get('active_id')
        record = self.env['hospital.accreditation'].browse(active_id)
        record.state = self.decision
        if self.decision == 'approved':
            record.struttura_da_accreditare_id.is_accreditata = True


