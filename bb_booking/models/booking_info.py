#copyright © Simone Tullino 08/11
from odoo import models, fields, api

class roombooking(models.Model):
    _inherit = ['account.move']

    refer = fields.Char(string='ID')
    checkin = fields.Date(string='Data di Check-in', tracking=True)
    checkout = fields.Date(string='Data di Check-out', tracking=True)
    totalGuest = fields.Integer(string='Ospiti Totali', tracking=True)
    totalChildren = fields.Integer(string='Totali Ragazzi', tracking=True)
    totalInfants = fields.Integer(string='Totali Neonati', tracking=True)
    totale_adulti = fields.Integer(string='totale adulti', tracking=True)
    soggiorno_input = fields.Html(string='Soggiorno', compute='_compute_soggiorno_input', sanitize=False, store=False)
    rooms = fields.Float(string='Numero stanza', tracking=True)
    roomGross = fields.Float(string='Costo stanza', tracking=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Stato', default='draft', readonly=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner', store=True, readonly=False, required=False)
    seq_fatt = fields.Char("sequenza fattura")
    email_utente = fields.Char(string='Email', tracking=True)
    telefono_utente = fields.Char(string='Telefono', tracking=True)
    nome_stanza_utente = fields.Char(string='Nome Stanza', tracking=True)
    nota_interna = fields.Text(string='Note interne', tracking=True)
    checkin_effettuato = fields.Char(string="Check_in effettuato", tracking=True)
    checkout_effettuato = fields.Char(string="Check_out effettuato", tracking=True)
    stato_del_pagamento = fields.Char(string="Stato del pagamento", tracking=True)
    tipo_di_pagamento = fields.Char(string="Tipo del pagamento", tracking=True)
    pulizia_camera = fields.Char(string="Pulizia camera", tracking=True)
    ultima_pulizia = fields.Char(string="Ultima pulizia", tracking=True)
    tipologia_camera = fields.Char(string='Tipologia Camera', tracking=True)
    nome_utente= fields.Char(string="Nome utente", tracking=True)
    indirizzo_utente = fields.Char(string="Indirizzo Utente", tracking=True)
    nazione_utente = fields.Char(string="Nazione Utente", tracking=True)
    cap_utente = fields.Char(string='CAP Utente', tracking=True)
    citta_utente= fields.Char(string="Città utente", tracking=True)

    




    # @api.model
    # def create(self, vals):
    #     vals["seq_fatt"] = self.env["ir.sequence"].next_by_code("account.move")
    #     return super(roombooking, self).create(vals)

    @api.depends('checkin', 'checkout', 'totalGuest')
    def _compute_soggiorno_input(self):
        for record in self:
            if record.checkin and record.checkout:
                # Imposta l'orario di check-in e check-out a mezzanotte
                checkin_date = fields.Date.from_string(record.checkin)
                checkout_date = fields.Date.from_string(record.checkout)
                delta = checkout_date - checkin_date
                num_notti = delta.days
                num_ospiti = record.totalGuest
                record.soggiorno_input = 2 * num_notti * num_ospiti
