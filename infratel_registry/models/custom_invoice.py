from odoo import models, fields, api


class CustomInvoices(models.Model):
    _inherit = "account.move"
    
    quadrature_possible = fields.Boolean(string="Quadratura Possibile")
    
    
    def trasmission(self):
        # Logica associata all'azione di "Invia per trasmissione"
        # Puoi implementare qui la logica desiderata quando l'utente fa clic sul pulsante "Invia per trasmissione"
        return True

    
    def sap(self):
        # Logica associata all'azione di "Invia a SAP"
        # Puoi implementare qui la logica desiderata quando l'utente fa clic sul pulsante "Invia a SAP"
        return True