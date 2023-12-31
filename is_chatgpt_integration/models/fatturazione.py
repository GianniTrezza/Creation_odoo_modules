from odoo import api, fields, models, _
import base64
from io import StringIO
import csv
import logging
from datetime import datetime


class File_Reader:

    def __init__(self):
        pass

    @staticmethod
    def read_file(path):
        #   print("[File_Reader] - reading file")
        file_object = open(path, "r")
        file_data = file_object.read()
        File_Reader.__close_file__(file_object)
        return file_data

    def __close_file__(file):
        #   print("[File_Reader] - closing file")
        file.close()


def convert_date_format(original_date):
    try:
        formatted_date = datetime.strptime(original_date.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {original_date}")
    return formatted_date


class ClientMappingLogger:
    LOG_PATH = 'C:\\Users\\giova\\odoo\\addons\\is_chatgpt_integration\\logs\\client_mapping.log'

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler(LOG_PATH, mode='a')
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)

    @staticmethod
    def get_logger():
        return ClientMappingLogger.logger


class TabellaFatture(models.Model):
    _inherit = 'account.move'

    addetto_vendite = fields.Char(string="Addetto vendite")
    documento_origine = fields.Char(string="Documento origine")

    data_file = fields.Binary(string='CSV File', required=True)
    filename = fields.Char(string='Filename')

    @api.model
    def create(self, vals):
        return super(TabellaFatture, self).create(vals)

    def _generate_client_ids(self, csv_data):
        clients = set(row[0] for row in csv_data)
        client_mapping = {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}
        logger = ClientMappingLogger.get_logger()
        for client, client_id in client_mapping.items():
            logger.info(f"Client: {client}, ID: {client_id}")
        return client_mapping

    def _generate_salesperson_ids(self, csv_data):
        salespeople = set(row[9] for row in csv_data)
        return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

    def _map_state_from_csv(self, csv_state):
        mapping = {
            "Bozza": "draft",
            "Aperta": "open",
            "Pagata": "paid",
            "Annullata": "cancelled",
        }
        return mapping.get(csv_state, "draft")

    def button_import(self):
        file_data = base64.b64decode(self.data_file)
        file_input = StringIO(file_data.decode('utf-8'))
        csv_file = list(csv.reader(file_input, delimiter=',', lineterminator='\n'))

        columns_mapping = {
            'Codice Fattura (Numero)': 'name',
            'Cliente': 'invoice_partner_display_name',
            'Data fattura': 'invoice_date',
            'Data scadenza': 'invoice_date_due',
            'No records': 'activity_ids',
            'Imponibile': 'amount_untaxed_signed',
            'Totale': 'amount_total_signed',
            'Importo dovuto': 'amount_total_in_currency_signed',
            'Stato –e fattura': 'payment_status',
            'Addetto vendite': 'partner_id',
        }

        client_ids = self._generate_client_ids(csv_file[1:])
        salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

        headers = csv_file[0]

        for row in csv_file[1:]:
            values = {}
            for header, value in zip(headers, row):
                field_name = columns_mapping.get(header)
                if field_name:
                    if field_name == 'invoice_date' or field_name == 'invoice_date_due':
                        values[field_name] = convert_date_format(value)
                    elif field_name == 'amount_untaxed_signed' or field_name == 'amount_total_signed' or field_name == 'amount_total_in_currency_signed':
                        values[field_name] = float(value) if value else 0.0
                    elif field_name == 'partner_id':
                        values[field_name] = client_ids[value]
                    elif field_name == 'addetto_vendite':
                        values[field_name] = salesperson_ids[value]
                    elif field_name == 'payment_status':
                        values[field_name] = self._map_state_from_csv(value)
                    else:
                        values[field_name] = value

            self.env['account.move'].create(values)
        
