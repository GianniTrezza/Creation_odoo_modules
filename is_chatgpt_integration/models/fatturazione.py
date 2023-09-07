from odoo import api, fields, models, _
# import base64
import csv
import os
from odoo.exceptions import ValidationError




class TabellaFatture(models.Model):
    _name = 'tabella.fatture'
    _description = 'Tabella Fatture di Unitiva'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "data_fattura desc"
    _order = "numero desc"

    # cliente_id = fields.Char(string='ID Cliente', readonly=True, copy=False , default=lambda self: _('New'))
    cliente_id = fields.Char(string='ID Cliente', readonly=True, copy=False, default=lambda self: _('Trezza'))
    data_fattura = fields.Date(string="Data fattura")
    numero = fields.Char(string="Numero")
    addetto_vendite = fields.Char(string="Addetto vendite")
    data_scadenza = fields.Date(string="Data scadenza")
    documento_origine = fields.Char(string="Documento origine")
    insoluta = fields.Boolean(string="Insoluta")
    imponibile = fields.Float(string="Imponibile")
    imposta = fields.Float(string="Imposta")
    totale = fields.Float(string="Totale")
    importo_dovuto = fields.Float(string="Importo dovuto")
    stato_efattura = fields.Selection([
        ('draft', 'Bozza'),
        ('open', 'Aperta'),
        ('paid', 'Pagata'),
        ('cancelled', 'Annullata')
    ], string="Stato e-fattura")
    stato = fields.Selection([
        ('draft', 'Bozza'),
        ('recorded', 'Registrato'),
        ('approved', 'Approvato')
    ], string="Stato", default='draft')

    @api.model
    def create(self, vals):
        if not vals.get('cliente_id'):
            vals['cliente_id'] = self.env['ir.sequence'].next_by_code('tabella.fatture.sequence')
        return super(TabellaFatture, self).create(vals)

class TabellaFattureImportWizard(models.TransientModel):
    _name = 'tabella.fatture.import.wizard'

    path = fields.Char(string='File Path', default='C:\\Users\\giova\\OneDrive\\Desktop\\tabella_fatture.csv', required=True, readonly= True)
    filename = fields.Char(string='Filename')

    def _generate_client_ids(self, csv_data):
        clients = set(row[0] for row in csv_data)
        return {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}

    def _generate_salesperson_ids(self, csv_data):
        salespeople = set(row[3] for row in csv_data)
        return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

    def button_import(self):
        self.ensure_one()

        if not os.path.exists(self.path):
            raise ValidationError(_("The provided file path does not exist."))

        with open(self.path, 'r', encoding='utf-8') as file:
            csv_file = list(csv.reader(file, delimiter=',', lineterminator='\n'))

        

        client_ids = self._generate_client_ids(csv_file[1:])
        salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

        for row in csv_file[1:]:
            salesperson_id = salesperson_ids[row[3].strip()]

            values = {
                'cliente_id': client_ids[row[0]],
                'data_fattura': row[1],
                'numero': row[2],
                'addetto_vendite': salesperson_id,
                'data_scadenza': row[4],
                'documento_origine': row[5],
                'insoluta': True if row[6] == 'Insoluta' else False,
                'imponibile': float(row[7]),
                'imposta': float(row[8]),
                'totale': float(row[9]),
                'importo_dovuto': float(row[10]),
                'stato_efattura': 'open' if row[11] == 'Aperta' else ('paid' if row[11] == 'Pagata' else 'draft')
            }
            self.env['tabella.fatture'].create(values)

#CODICE CHE MIGLIORI L'IMPORT DEL CSV FILE 
# from odoo import api, fields, models, _
# import base64
# import csv
# from io import StringIO
# import os
# import logging

# _logger = logging.getLogger(__name__)

# class TabellaFatture(models.Model):
#     _name = 'tabella.fatture'
#     _description = 'Tabella Fatture di Unitiva'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _order = "data_fattura desc"

#     cliente_id = fields.Char(string='ID Cliente', readonly=True, copy=False, default=lambda self: _('Trezza'))
#     data_fattura = fields.Date(string="Data fattura")
#     numero = fields.Char(string="Numero")
#     addetto_vendite = fields.Char(string="Addetto vendite")
#     data_scadenza = fields.Date(string="Data scadenza")
#     documento_origine = fields.Char(string="Documento origine")
#     insoluta = fields.Boolean(string="Insoluta")
#     imponibile = fields.Float(string="Imponibile")
#     imposta = fields.Float(string="Imposta")
#     totale = fields.Float(string="Totale")
#     importo_dovuto = fields.Float(string="Importo dovuto")
#     stato_efattura = fields.Selection([
#         ('draft', 'Bozza'),
#         ('open', 'Aperta'),
#         ('paid', 'Pagata'),
#         ('cancelled', 'Annullata')
#     ], string="Stato e-fattura", default='draft')
#     stato = fields.Selection([
#         ('draft', 'Bozza'),
#         ('recorded', 'Registrato'),
#         ('approved', 'Approvato')
#     ], string="Stato", default='draft')

#     @api.model
#     def create(self, vals):
#         if not vals.get('cliente_id'):
#             vals['cliente_id'] = self.env['ir.sequence'].next_by_code('tabella.fatture.sequence')
#         return super(TabellaFatture, self).create(vals)

# class TabellaFattureImportWizard(models.TransientModel):
#     _name = 'tabella.fatture.import.wizard'
    
#     data_file = fields.Binary(string='CSV File', required=True)
#     filename = fields.Char(string='Filename')

#     def _generate_client_ids(self, csv_data):
#         clients = set(row[0] for row in csv_data)
#         return {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}

#     def _generate_salesperson_ids(self, csv_data):
#         salespeople = set(row[3] for row in csv_data)
#         return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

#     def button_import(self, csv_content=None):
#         self.ensure_one()

#         if not csv_content:
#             _logger.info("Importing from uploaded file...")
#             file_data = base64.b64decode(self.data_file)
#             csv_content = file_data.decode('utf-8')
#         else:
#             _logger.info("Importing from provided csv_content...")
        
#         file_input = StringIO(csv_content)
#         csv_file = list(csv.reader(file_input, delimiter=',', lineterminator='\n'))

#         client_ids = self._generate_client_ids(csv_file[1:])
#         salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

#         for row in csv_file[1:]:
#             salesperson_id = salesperson_ids[row[3].strip()]

#             values = {
#                 'cliente_id': client_ids[row[0]],
#                 'data_fattura': row[1],
#                 'numero': row[2],
#                 'addetto_vendite': salesperson_id,
#                 'data_scadenza': row[4],
#                 'documento_origine': row[5],
#                 'insoluta': True if row[6] == 'Insoluta' else False,
#                 'imponibile': float(row[7]),
#                 'imposta': float(row[8]),
#                 'totale': float(row[9]),
#                 'importo_dovuto': float(row[10]),
#                 'stato_efattura': 'open' if row[11] == 'Aperta' else ('paid' if row[11] == 'Pagata' else 'draft')
#             }
#             self.env['tabella.fatture'].create(values)

#     @api.model
#     def import_from_path(self):
#         _logger.info("Attempting to import from path...")
#         path = "C:\\Users\\giova\\OneDrive\\Desktop\\tabella_fatture.csv"
#         if os.path.exists(path):
#             _logger.info(f"File found at {path}...")
#             with open(path, 'r', encoding='utf-8') as file:
#                 csv_content = file.read()
#                 wizard = self.create({'filename': 'tabella_fatture.csv'})
#                 wizard.button_import(csv_content=csv_content)
#         else:
#             _logger.warning(f"File not found at {path}!")

 





  