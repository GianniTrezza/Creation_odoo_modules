
# # *****************************NEW CODE: TENTATIVO DI CORRISPONDENZA TRA IL NOME DEI CAMPI CREATI CON QUELLI AGGIORNATI NEL CHATTER ***************
# from odoo import http, models
# from odoo import _
# from odoo.http import request, Response
# import json
# import datetime
# import requests
# import logging


# # _logger = logging.getLogger(__name__)


# field_labels = {
#     'checkin': 'Checkin',
#     'checkout': 'Checkout',
#     'totalGuest': 'Numero totale ospiti',
#     'totalChildren': 'Totale Bambini',
#     'totalInfants': 'Totale Neonati',
#     'rooms': 'Numero camere',
#     'roomGross': 'Prezzo Unitario',
#     'roomName': 'Nome Stanza',
#     'ref': 'Riferimento',
#     'channelNotes': 'Note aggiuntive',
#     'partner_id': 'ID Cliente',
#     'email': 'Email Cliente',
#     'piattaforma': 'Piattaforma di Prenotazione',
#     'invoicedate': 'Data Fattura',
#     'pmsProduct': 'Prodotto PMS',
#     'PaymentStatus': 'Stato del pagamento',
#     'PaymentType': 'Tipo di pagamento',
#     'effectiveCheckin': 'Check in effettuato',
#     'effectiveCheckout': 'Check out effettuato',
#     'privateNotes': 'Note interne'
# }
# def generate_message_body(data, room_cleaning_data, field_labels, changes=None, is_update=False, include_chatter_fields=False):
#     lines = []
#     has_changes = False

#     for field, label in field_labels.items():
#         if field in data and (include_chatter_fields or field not in ['privateNotes', 'effectiveCheckin', 'effectiveCheckout']):
#             new_value = data[field]
#             if is_update and changes and field in changes:
#                 old_value = changes[field]['old']
#                 if old_value != new_value:
#                     has_changes = True
#                     lines.append(f"{label}: {old_value} > {new_value}")

#     if has_changes:
#         if room_cleaning_data:
#             clean_status = 'Clean' if room_cleaning_data['clean'] else 'Not Clean'
#             lines.append(f"Room Cleaning Status: {clean_status}")
#             lines.append(f"Last Cleaning Date: {room_cleaning_data['lastCleaningDate']}")
#             lines.append(f"Nome specifico stanza: {room_cleaning_data['name']}")

#     if lines:
#         title = "Dati aggiornati:" if is_update else "Dati di fatturazione creati:"
#         return f"<p><b><font size='4' face='Arial'>{title}</font></b><br>" + "<br>".join(lines) + "</p>"
#     else:
#         return None

# # def generate_message_body(data, room_cleaning_data, field_labels, changes=None, is_update=False, include_chatter_fields=False):
# #     lines = []
# #     for field, label in field_labels.items():
# #         if field in data and (include_chatter_fields or field not in ['privateNotes', 'effectiveCheckin', 'effectiveCheckout']):
# #             new_value = data[field]
# #             formatted_new_value = new_value.strftime('%Y-%m-%d') if isinstance(new_value, datetime.date) else new_value
# #             if is_update and changes and field in changes:
# #                 old_value = changes[field]['old']
# #                 formatted_old_value = old_value.strftime('%Y-%m-%d') if isinstance(old_value, datetime.date) else old_value
# #                 lines.append(f"{label}: {formatted_old_value} > {formatted_new_value}")
# #             elif not is_update:
# #                 lines.append(f"{label}: {formatted_new_value}")
# #     # Adding room cleaning data if available
# #         # Aggiunta di controllo sul tipo di room_cleaning_data
# #     if isinstance(room_cleaning_data, dict):
# #         clean_status = 'Clean' if room_cleaning_data.get('clean') else 'Not Clean'
# #         lines.append(f"Room Cleaning Status: {clean_status}")
# #         lines.append(f"Last Cleaning Date: {room_cleaning_data.get('lastCleaningDate')}")
# #         lines.append(f"Nome specifico stanza: {room_cleaning_data.get('name')}")
# #     else:
# #         lines.append("Room Cleaning Data: Not available")
# #     if room_cleaning_data:
# #         clean_status = 'Clean' if room_cleaning_data['clean'] else 'Not Clean'
# #         lines.append(f"Room Cleaning Status: {clean_status}")
# #         lines.append(f"Last Cleaning Date: {room_cleaning_data['lastCleaningDate']}")
# #         lines.append(f"Nome specifico stanza: {room_cleaning_data['name']}")

# #     title = "Dati aggiornati:" if is_update else "Dati di fatturazione creati:"
# #     return f"<p><b><font size='4' face='Arial'>{title}</font></b><br>" + "<br>".join(lines) + "</p>"

# _logger = logging.getLogger(__name__)
# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"


# def get_access_token():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"

#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }

#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None


# # Ottieni il token di accesso
# access_token = get_access_token()
# if access_token:
#     print(f"Token di accesso ottenuto con successo: {access_token}")
# else:
#     print("Errore nell'ottenere il token di accesso.")

# def fetch_room_cleaning_details(pms_product_id, token):
#     url = "https://api.octorate.com/connect/rest/v1/pms"
#     headers = {
#         'accept': 'application/json',
#         'Authorization': f'Bearer {token}'
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json().get("data", [])
#         for room in data:
#             if room["id"] == pms_product_id:
#                 return {
#                     'clean': room.get("clean", False),
#                     'lastCleaningDate': room.get("lastCleaningDate"),
#                     'name': room.get("name")
#                 }
#         return {'clean': False, 'lastCleaningDate': None, 'name': None}
#     else:
#         _logger.error(f"Failed to fetch room details: {response.status_code} - {response.text}")
#         return {'clean': False, 'lastCleaningDate': None, 'name': None}




# class RoomBookingController(http.Controller):

#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         data_dict = json.loads(json_data)
#         content = json.loads(data_dict.get("content"))
#         create_time_str = data_dict.get("createTime")

#         try:
#             create_time = datetime.datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%SZ[UTC]') if create_time_str else None
#         except ValueError:
#             return Response("Invalid date format for createTime", content_type='text/plain', status=400)

#         if not content.get("refer") or not content.get("guests"):
#             return Response("Missing required fields", content_type='text/plain', status=400)

#         checkin_str = content.get("guests")[0].get("checkin")
#         checkout_str = content.get("guests")[0].get("checkout")
        
#         try:
#             checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
#             checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
#         except ValueError:
#             return Response("Invalid date format", content_type='text/plain', status=400)

#         reservation_data = {
#             'partner_id': content.get("guestsList"),
#             'email': content.get("guestMailAddress"),
#             'refer': content.get("refer"),
#             'ref': content.get('pmsProduct'),
#             'roomName': content.get('roomName'),
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'channelNotes': content.get("channelNotes"),
#             'totalGuest': content.get("totalGuest"),
#             'totalChildren': content.get("totalChildren"),
#             'totalInfants': content.get("totalInfants"),
#             'rooms': content.get("rooms"),
#             'roomGross': content.get("roomGross"),
#             'invoicedate': create_time,
#             'piattaforma': content.get("channelName"),
#             'effectiveCheckin':content.get("effectiveCheckin"),
#             'effectiveCheckout':content.get("effectiveCheckout"), 
#             'note interne':content.get("privateNotes"),
#             'Stato del pagamento':content.get("PaymentStatus"), 
#             'Tipo di pagamento':content.get("PaymentType")
#         }
        
        
#         event_type = data_dict.get("type")
#         response_data = {}

#         if event_type == "RESERVATION_CREATED":
#             invoice_details = self.calculate_invoice_details(reservation_data)
#             self.create_invoice(reservation_data, invoice_details)
#             response_data.update(invoice_details)
            
            
#         elif event_type == "RESERVATION_CHANGE":
#             refer_id = reservation_data.get('refer')
#             nome_cliente=reservation_data.get('partner_id')

#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id), ('partner_id', '=', nome_cliente)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
#             reservation_data.pop('email', None)
#             if 'email' in request.env['account.move']._fields:
#                 invoice_record.sudo().write({'email': content.get("guestMailAddress")})
#             # Aggiungi il messaggio di pulizia solo se invoice_record è stato definito
#             if invoice_record:
#                 pms_product_id = content.get("pmsProduct")
#                 clean, last_cleaning_date, name = fetch_room_cleaning_details(pms_product_id, token=access_token)
#                 cleaning_details_message = f"Room Cleaning Status: {'Clean' if clean else 'Not Clean'}\n" \
#                                         f"Last Cleaning Date: {last_cleaning_date}"\
#                                         f"Nome specifico stanza: {name}"
#                 _logger.info(f"Room cleaning data before passing to function: {cleaning_details_message}")

#                 invoice_message_body = generate_message_body(reservation_data, cleaning_details_message, field_labels, changes=None, is_update=True, include_chatter_fields=True)
#                 invoice_record.message_post(body=invoice_message_body, message_type='comment')
#                 cleaning_details = {
#                     'cleaning_status': 'Clean' if clean else 'Not Clean',
#                     'last_cleaning_date': last_cleaning_date,
#                     'name': name
#                 }
#                 response_data.update({'cleaning_details': cleaning_details})
# # LALALA
            

#             self.update_invoice_lines(invoice_record, reservation_data)
#             response_data.update({
#                 "partner_id": invoice_record.partner_id.name,
#                 "move_id": invoice_record.id,
#                 "checkin": invoice_record.checkin.strftime('%Y-%m-%d') if isinstance(invoice_record.checkin, datetime.date) else invoice_record.checkin,
#                 "checkout": invoice_record.checkout.strftime('%Y-%m-%d') if isinstance(invoice_record.checkout, datetime.date) else invoice_record.checkout,
#                 "invoice_date": invoice_record.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(invoice_record.invoice_date, datetime.datetime) else invoice_record.invoice_date,
#                 "totalGuest": invoice_record.totalGuest,
#                 "totalChildren": invoice_record.totalChildren,
#                 "totalInfants": invoice_record.totalInfants,
#                 "rooms": invoice_record.rooms,
#                 "product_id": invoice_record.roomName,
#                 "note aggiuntive": invoice_record.channelNotes,
#                 "ref":invoice_record.pmsProduct,
#                 "state": invoice_record.state,
#                 "Piattaforma di prenotazione" : reservation_data["piattaforma"],
#                 "Checkin_effettuato" : reservation_data["effectiveCheckin"],
#                 "Checkout_effettuato" : reservation_data["effectiveCheckout"],
#                 "Note interne" : reservation_data["note interne"],
#                 'cleaning_details': cleaning_details
#             })

#         elif event_type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
#             refer_id = reservation_data.get('refer')
#             checkout_id=reservation_data.get('checkout')
            
#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)

#             if invoice_record.checkout != checkout_id:
#                 return Response(f"Invoice found with refer: {refer_id}, but with different checkout date.", content_type='text/plain', status=400)

#             new_state = 'cancel' if event_type == 'RESERVATION_CANCELLED' else 'posted'
#             invoice_record.sudo().write({'state': new_state})
#         else:
#             return Response("Invalid event type", content_type='text/plain', status=400)
        
#         for key, value in response_data.items():
#             if isinstance(value, datetime.date):
#                 response_data[key] = value.strftime('%Y-%m-%d')

#         return Response(json.dumps(response_data), content_type='application/json', status=200)

#     def calculate_invoice_details(self, reservation_data):
#         nome_ospite= reservation_data['partner_id']
#         checkin_date = reservation_data['checkin']
        
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         num_ospiti = reservation_data['totalGuest']

#         tourist_tax_quantity = num_notti * num_ospiti * 2
        
#         booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
#         booking_quantity = reservation_data['rooms']
#         booking_price_unit = reservation_data['roomGross']
#         nome_stanza = reservation_data['roomName']
    
#         return {
#             "Orario creazione prenotazione": reservation_data["invoicedate"].strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(reservation_data["invoicedate"], datetime.datetime) else reservation_data["invoicedate"],
#             "Nome ospite": nome_ospite,
#             "Valore tassa turistica": tourist_tax_quantity,
#             "Identificativo della prenotazione": booking_name,
#             "Numero stanze": booking_quantity,
#             "Costo stanza": booking_price_unit,
#             "Tipologia stanza": nome_stanza,
#             "Numero identificativo Camera": reservation_data["ref"]
            
#         }

#     def create_invoice(self, reservation_data, invoice_details):
#         tax_0_percent = None
#         partner_name = reservation_data['partner_id']
#         nome_stanza = reservation_data['roomName']
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         partner = request.env['res.partner'].sudo().with_context(partner_display='invoice_partner_display_name').search([('name', '=', partner_name)], limit=1)
#         team_vendite = request.env['crm.team'].sudo().search([('name','=',reservation_data["piattaforma"])], limit=1)
#         if not team_vendite:
#             team_vendite = request.env['crm.team'].sudo().create({'name': reservation_data["piattaforma"]})

#         if not partner:
#             partner = request.env['res.partner'].sudo().create({
#                 'name': partner_name,
#                 'email': reservation_data.get('email'),
#                 'customer_rank': 1
#             })

#         room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)])
#         if not room_product:
#             room_product = request.env['product.product'].sudo().create({'name': nome_stanza})
            
#         tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
#         if not tassa_soggiorno_product:
#             tax_0_percent = request.env['account.tax'].sudo().search(
#                 [('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)],
#                 limit=1
#             )
#             if not tax_0_percent:
#                 raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
            
#             vals = {
#                 'name': 'Tassa di Soggiorno',
#                 'type': 'service',
#             }
            
#             if tax_0_percent is not None:
#                 vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]

#             tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)
        
#         customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
#         account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
#         journal_id = customer_invoice_journal.id
#         partner_values = {
#             'name': reservation_data["partner_id"],
#             'email': reservation_data["email"],
#         }

#         partner = request.env['res.partner'].sudo().create(partner_values)
#         partner_display_name = partner.name_get()[0][1] if partner else "Nuovo Partner"
        
#         invoice_values = {
#             'journal_id': journal_id,
#             'move_type': 'out_invoice',
#             'ref': reservation_data['ref'],
#             'partner_id': partner.id,
#             'invoice_partner_display_name': partner_display_name,
#             'checkin': reservation_data['checkin'],
#             'checkout': reservation_data['checkout'],
#             'refer': reservation_data['refer'],
#             'totalGuest': reservation_data['totalGuest'],
#             'totalChildren': reservation_data['totalChildren'],
#             'rooms': reservation_data['rooms'],
#             'roomGross': reservation_data['roomGross'],
#             'invoice_date': reservation_data['invoicedate'],
#             'channelNotes': reservation_data['channelNotes'],
#             'team_id': team_vendite.id
#         }
#         invoice_record = request.env['account.move'].sudo().create(invoice_values)
#         room_cleaning_data = None
#         invoice_message_body = generate_message_body(reservation_data, room_cleaning_data, field_labels, changes=None, is_update=False, include_chatter_fields=True)
#         invoice_record.message_post(body=invoice_message_body, message_type='comment')

#         booking_line_values = {
#             'move_id': invoice_record.id,
#             'product_id': room_product.id,
#             'name': invoice_details['Identificativo della prenotazione'],
#             'quantity': reservation_data['rooms'],
#             'price_unit': invoice_details['Costo stanza'],
#             'account_id': account_id
#         }
#         request.env['account.move.line'].sudo().create(booking_line_values)

#         tourist_tax_line_values = {
#             'move_id': invoice_record.id,
#             'product_id': tassa_soggiorno_product.id,
#             'name': "Tassa soggiorno",
#             'quantity': reservation_data['totalGuest']*num_notti,
#             'price_unit': 2,
#             'account_id': account_id
#         }
#         request.env['account.move.line'].sudo().create(tourist_tax_line_values)

#     def update_invoice_lines(self, invoice_record, reservation_data):
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days

#         updated_data = {
#             'invoice_date': reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.datetime) else reservation_data['invoicedate'],
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'totalGuest': reservation_data['totalGuest'],
#             'totalChildren': reservation_data['totalChildren'],
#             'rooms': reservation_data['rooms'],
#             'roomGross': reservation_data['roomGross'],
#             'ref': reservation_data['ref'],
#             'channelNotes': reservation_data['channelNotes'],
#             'check in effettuato': reservation_data['effectiveCheckin'],
#             'check out effettuato': reservation_data['effectiveCheckout'],
#             'check out effettuato': reservation_data['effectiveCheckout']
#         }

#         changes = {}
#         for field, new_value in updated_data.items():
#             if field in field_labels and field in reservation_data:
#                 old_value = getattr(invoice_record, field, None)
#                 if new_value != old_value:
#                     changes[field] = {'old': old_value, 'new': new_value}
#                     invoice_record.sudo().write({field: new_value})

#         booking_name = f"Prenotazione {reservation_data['refer']} dal {checkin_date} al {checkout_date}"
#         for line in invoice_record.invoice_line_ids:
#             if line.product_id.name == reservation_data['roomName']:
#                 line.write({'name': booking_name, 'price_unit': reservation_data['roomGross'], 'quantity': reservation_data['rooms']})
#             elif line.product_id.name == 'Tassa di Soggiorno':
#                 line.write({'quantity': reservation_data['totalGuest'] * num_notti, 'price_unit': 2})
#         room_cleaning_data = None
#         if changes:
#             invoice_message_body = generate_message_body(reservation_data, room_cleaning_data, field_labels, changes, is_update=True, include_chatter_fields=True)
#             invoice_record.message_post(body=invoice_message_body, message_type='comment')

# ****************************VECCHIO CODICE***************************************************

# *****************************NEW CODE: TENTATIVO DI CORRISPONDENZA TRA IL NOME DEI CAMPI CREATI CON QUELLI AGGIORNATI NEL CHATTER ***************
# from odoo import http, models
# from odoo import _
# from odoo.http import request, Response
# import json
# import datetime
# import requests
# import logging
# import time


# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# _logger = logging.getLogger(__name__)



# # _logger = logging.getLogger(__name__)


# field_labels = {
#     'checkin': 'Checkin',
#     'checkout': 'Checkout',
#     'totalGuest': 'Numero totale ospiti',
#     'totalChildren': 'Totale Bambini',
#     'totalInfants': 'Totale Neonati',
#     'rooms': 'Numero camere',
#     'roomGross': 'Prezzo Unitario',
#     'roomName': 'Nome Stanza',
#     'ref': 'Riferimento',
#     'channelNotes': 'Note aggiuntive',
#     'partner_id': 'ID Cliente',
#     'email': 'Email Cliente',
#     'piattaforma': 'Piattaforma di Prenotazione',
#     'invoicedate': 'Data Fattura',
#     'pmsProduct': 'Prodotto PMS',
#     'PaymentStatus': 'Stato del pagamento',
#     'PaymentType': 'Tipo di pagamento',
#     'effectiveCheckin': 'Check in effettuato',
#     'effectiveCheckout': 'Check out effettuato',
#     'privateNotes': 'Note interne'
# }

# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"



# access_token_info = {'token': None, 'expires_at': None}

# def get_access_token(force_refresh=False):
#     global access_token_info

#     if access_token_info['token'] and not force_refresh:
#         if time.time() < access_token_info['expires_at']:
#             return access_token_info['token']

    
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}

#     # Effettua la richiesta per ottenere un nuovo token
#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code == 200:
#         token_data = response.json()
#         access_token_info['token'] = token_data.get("access_token")
#         # Assumi che il token scada dopo 1 ora (3600 secondi) - adatta secondo la documentazione API
#         access_token_info['expires_at'] = time.time() + 3600
#         return access_token_info['token']
#     else:
#         # Gestione dell'errore
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None


# # Ottieni il token di accesso
# access_token = get_access_token()
# if access_token:
#     print(f"Il token è stato ottenuto con successo, tuttavia questo token non funziona nell'ottenimento dei dati sulle pulizie : {access_token}")
# else:
#     print("Errore nell'ottenere il token di accesso.")



# # def generate_message_body(data, field_labels, is_update=False, include_chatter_fields=False):
# #     lines = []
# #     for field, label in field_labels.items():
# #         if field in data and (include_chatter_fields or field not in ['privateNotes', 'effectiveCheckin', 'effectiveCheckout']):
# #             value = data[field]
# #             formatted_value = value.strftime('%Y-%m-%d') if isinstance(value, datetime.date) else value
# #             lines.append(f"{label}: {formatted_value}")

# #     if is_update:
# #         title = "Dati aggiornati:"
# #     else:
# #         title = "Dati di fatturazione creati:"

# #     return f"<p><b><font size='4' face='Arial'>{title}</font></b><br>" + "<br>".join(lines) + "</p>"
# def generate_message_body(data, field_labels, changes=None, is_update=False, include_chatter_fields=False):
#     lines = []
#     for field, label in field_labels.items():
#         if field in data and (include_chatter_fields or field not in ['privateNotes', 'effectiveCheckin', 'effectiveCheckout']):
#             value = data[field]
#             formatted_value = value.strftime('%Y-%m-%d') if isinstance(value, datetime.date) else value
#             if not is_update or (is_update and field in changes):
#                 lines.append(f"{label}: {formatted_value}")

#     title = "Dati aggiornati:" if is_update else "Dati di fatturazione creati:"
#     return f"<p><b><font size='4' face='Arial'>{title}</font></b><br>" + "<br>".join(lines) + "</p>"


# _logger = logging.getLogger(__name__)
# def fetch_room_cleaning_details(pms_product_id, token):
#     url = "https://api.octorate.com/connect/rest/v1/pms"
#     headers = {'accept': 'application/json', 'Authorization': f'Bearer {token}'}

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Questo solleverà un'eccezione per risposte non 200
#         data = response.json().get("data", [])
#         for room in data:
#             if room["id"] == pms_product_id:
#                 return room.get("clean"), room.get("lastCleaningDate"), room.get("name")
#     except requests.exceptions.HTTPError as errh:
#         _logger.error(f"HTTP Error: {errh}")
#     except requests.exceptions.ConnectionError as errc:
#         _logger.error(f"Error Connecting: {errc}")
#     except requests.exceptions.Timeout as errt:
#         _logger.error(f"Timeout Error: {errt}")
#     except requests.exceptions.RequestException as err:
#         _logger.error(f"Error: {err}")

#     return None, None, None



# class RoomBookingController(http.Controller):

#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         data_dict = json.loads(json_data)
#         content = json.loads(data_dict.get("content"))
#         create_time_str = data_dict.get("createTime")

        
#         try:
#             create_time = datetime.datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%SZ[UTC]') if create_time_str else None
#         except ValueError:
#             return Response("Invalid date format for createTime", content_type='text/plain', status=400)

#         if not content.get("refer") or not content.get("guests"):
#             return Response("Missing required fields", content_type='text/plain', status=400)

#         checkin_str = content.get("guests")[0].get("checkin")
#         checkout_str = content.get("guests")[0].get("checkout")
        
#         try:
#             checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
#             checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
#         except ValueError:
#             return Response("Invalid date format", content_type='text/plain', status=400)
        
#         start_validity_date = datetime.datetime(2024, 1, 1).date()
#         end_validity_date = datetime.datetime(2024, 1, 1).date()
#         if checkin_date and checkin_date < start_validity_date:
#             _logger.info(f"Il checkin per la data seguente: {checkin_date} è stato ignorato")
#             return Response("Check in ignorato", content_type='text/plain', status=200)
#         elif checkout_date and checkout_date < end_validity_date:
#             _logger.info(f"Il checkout per la data seguente: {checkout_date} è stato ignorato")
#             return Response("Check out ignorato", content_type='text/plain', status=200)

#         reservation_data = {
#             'partner_id': content.get("guestsList"),
#             'email': content.get("guestMailAddress"),
#             'refer': content.get("refer"),
#             'ref': content.get('pmsProduct'),
#             'roomName': content.get('roomName'),
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'channelNotes': content.get("channelNotes"),
#             'totalGuest': content.get("totalGuest"),
#             'totalChildren': content.get("totalChildren"),
#             'totalInfants': content.get("totalInfants"),
#             'rooms': content.get("rooms"),
#             'roomGross': content.get("roomGross"),
#             'invoicedate': create_time,
#             'piattaforma': content.get("channelName"),
#             'effectiveCheckin':content.get("effectiveCheckin"),
#             'effectiveCheckout':content.get("effectiveCheckout"), 
#             'note interne':content.get("privateNotes"),
#             'Stato del pagamento':content.get("PaymentStatus"), 
#             'Tipo di pagamento':content.get("PaymentType")
#         }
        
        
#         event_type = data_dict.get("type")
#         response_data = {}

#         if event_type == "RESERVATION_CREATED":
#             invoice_details = self.calculate_invoice_details(reservation_data)
#             self.create_invoice(reservation_data, invoice_details)
#             response_data.update(invoice_details)
            
            
#         elif event_type == "RESERVATION_CHANGE":
#             refer_id = reservation_data.get('refer')
#             nome_cliente=reservation_data.get('partner_id')

#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id), ('partner_id', '=', nome_cliente)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
#             reservation_data.pop('email', None)
#             if 'email' in request.env['account.move']._fields:
#                 invoice_record.sudo().write({'email': content.get("guestMailAddress")})
#             # Aggiungi il messaggio di pulizia solo se invoice_record è stato definito
#             if invoice_record:
#                 pms_product_id = content.get("pmsProduct")
#                 clean, last_cleaning_date, name = fetch_room_cleaning_details(pms_product_id, token=access_token)
#                 cleaning_details_message = f"Room Cleaning Status: {'Clean' if clean else 'Not Clean'}\n" \
#                                         f"Last Cleaning Date: {last_cleaning_date}"\
#                                         f"Nome specifico stanza: {name}"
                
#                 invoice_record.message_post(body=cleaning_details_message, message_type='comment')
#                 cleaning_details = {
#                     'cleaning_status': 'Clean' if clean else 'Not Clean',
#                     'last_cleaning_date': last_cleaning_date,
#                     'name': name
#                 }
#                 response_data.update({'cleaning_details': cleaning_details})
# # LALALA
            

#             self.update_invoice_lines(invoice_record, reservation_data)
#             response_data.update({
#                 "partner_id": invoice_record.partner_id.name,
#                 "move_id": invoice_record.id,
#                 "checkin": invoice_record.checkin.strftime('%Y-%m-%d') if isinstance(invoice_record.checkin, datetime.date) else invoice_record.checkin,
#                 "checkout": invoice_record.checkout.strftime('%Y-%m-%d') if isinstance(invoice_record.checkout, datetime.date) else invoice_record.checkout,
#                 "invoice_date": invoice_record.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(invoice_record.invoice_date, datetime.datetime) else invoice_record.invoice_date,
#                 "totalGuest": invoice_record.totalGuest,
#                 "totalChildren": invoice_record.totalChildren,
#                 "totalInfants": invoice_record.totalInfants,
#                 "rooms": invoice_record.rooms,
#                 "product_id": invoice_record.roomName,
#                 "note aggiuntive": invoice_record.channelNotes,
#                 "ref":invoice_record.pmsProduct,
#                 "state": invoice_record.state,
#                 "Piattaforma di prenotazione" : reservation_data["piattaforma"],
#                 "Checkin_effettuato" : reservation_data["effectiveCheckin"],
#                 "Checkout_effettuato" : reservation_data["effectiveCheckout"],
#                 "Note interne" : reservation_data["note interne"],
#                 'cleaning_details': cleaning_details
#             })
#             # 'effectiveCheckin':content.get("effectiveCheckin"),
#             # 'effectiveCheckout':content.get("effectiveCheckout"), 
#             # 'note interne':content.get("privateNotes"),
#             # 'Stato del pagamento':content.get("PaymentStatus"), 
#             # 'Tipo di pagamento':content.get("PaymentType")

#         elif event_type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
#             refer_id = reservation_data.get('refer')
#             checkout_id=reservation_data.get('checkout')
            
#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)

#             if invoice_record.checkout != checkout_id:
#                 return Response(f"Invoice found with refer: {refer_id}, but with different checkout date.", content_type='text/plain', status=400)

#             new_state = 'cancel' if event_type == 'RESERVATION_CANCELLED' else 'posted'
#             invoice_record.sudo().write({'state': new_state})
#         else:
#             return Response("Invalid event type", content_type='text/plain', status=400)
        
#         for key, value in response_data.items():
#             if isinstance(value, datetime.date):
#                 response_data[key] = value.strftime('%Y-%m-%d')

#         return Response(json.dumps(response_data), content_type='application/json', status=200)

#     def calculate_invoice_details(self, reservation_data):
#         nome_ospite= reservation_data['partner_id']
#         checkin_date = reservation_data['checkin']
        
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         num_ospiti = reservation_data['totalGuest']

#         tourist_tax_quantity = num_notti * num_ospiti * 2
        
#         booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
#         booking_quantity = reservation_data['rooms']
#         booking_price_unit = reservation_data['roomGross']
#         nome_stanza = reservation_data['roomName']
    
#         return {
#             "Orario creazione prenotazione": reservation_data["invoicedate"].strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(reservation_data["invoicedate"], datetime.datetime) else reservation_data["invoicedate"],
#             "Nome ospite": nome_ospite,
#             "Valore tassa turistica": tourist_tax_quantity,
#             "Identificativo della prenotazione": booking_name,
#             "Numero stanze": booking_quantity,
#             "Costo stanza": booking_price_unit,
#             "Tipologia stanza": nome_stanza,
#             "Numero identificativo Camera": reservation_data["ref"]
            
#         }

#     def create_invoice(self, reservation_data, invoice_details):
#         tax_0_percent = None
#         partner_name = reservation_data['partner_id']
#         nome_stanza = reservation_data['roomName']
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         partner = request.env['res.partner'].sudo().with_context(partner_display='invoice_partner_display_name').search([('name', '=', partner_name)], limit=1)
#         team_vendite = request.env['crm.team'].sudo().search([('name','=',reservation_data["piattaforma"])], limit=1)
#         if not team_vendite:
#             team_vendite = request.env['crm.team'].sudo().create({'name': reservation_data["piattaforma"]})

#         if not partner:
#             partner = request.env['res.partner'].sudo().create({
#                 'name': partner_name,
#                 'email': reservation_data.get('email'),
#                 'customer_rank': 1
#             })

#         room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)])
#         if not room_product:
#             room_product = request.env['product.product'].sudo().create({'name': nome_stanza})
            
#         tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
#         if not tassa_soggiorno_product:
#             tax_0_percent = request.env['account.tax'].sudo().search(
#                 [('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)],
#                 limit=1
#             )
#             if not tax_0_percent:
#                 raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
            
#             vals = {
#                 'name': 'Tassa di Soggiorno',
#                 'type': 'service',
#             }
            
#             if tax_0_percent is not None:
#                 vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]

#             tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)
        
#         customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
#         account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
#         journal_id = customer_invoice_journal.id
#         partner_values = {
#             'name': reservation_data["partner_id"],
#             'email': reservation_data["email"],
#         }

#         partner = request.env['res.partner'].sudo().create(partner_values)
#         partner_display_name = partner.name_get()[0][1] if partner else "Nuovo Partner"
        
#         invoice_values = {
#             'journal_id': journal_id,
#             'move_type': 'out_invoice',
#             'ref': reservation_data['ref'],
#             'partner_id': partner.id,
#             'invoice_partner_display_name': partner_display_name,
#             'checkin': reservation_data['checkin'],
#             'checkout': reservation_data['checkout'],
#             'refer': reservation_data['refer'],
#             'totalGuest': reservation_data['totalGuest'],
#             'totalChildren': reservation_data['totalChildren'],
#             'rooms': reservation_data['rooms'],
#             'roomGross': reservation_data['roomGross'],
#             'invoice_date': reservation_data['invoicedate'],
#             'channelNotes': reservation_data['channelNotes'],
#             'team_id': team_vendite.id
#         }
#         invoice_record = request.env['account.move'].sudo().create(invoice_values)
#         invoice_message_body = generate_message_body(reservation_data, field_labels, changes=None, is_update=False, include_chatter_fields=True)
#         invoice_record.message_post(body=invoice_message_body, message_type='comment')

#         booking_line_values = {
#             'move_id': invoice_record.id,
#             'product_id': room_product.id,
#             'name': invoice_details['Identificativo della prenotazione'],
#             'quantity': reservation_data['rooms'],
#             'price_unit': invoice_details['Costo stanza'],
#             'account_id': account_id
#         }
#         request.env['account.move.line'].sudo().create(booking_line_values)

#         tourist_tax_line_values = {
#             'move_id': invoice_record.id,
#             'product_id': tassa_soggiorno_product.id,
#             'name': "Tassa soggiorno",
#             'quantity': reservation_data['totalGuest']*num_notti,
#             'price_unit': 2,
#             'account_id': account_id
#         }
#         request.env['account.move.line'].sudo().create(tourist_tax_line_values)

#     def update_invoice_lines(self, invoice_record, reservation_data):
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days

#         updated_data = {
#             'invoice_date': reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.datetime) else reservation_data['invoicedate'],
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'totalGuest': reservation_data['totalGuest'],
#             'totalChildren': reservation_data['totalChildren'],
#             'rooms': reservation_data['rooms'],
#             'roomGross': reservation_data['roomGross'],
#             'ref': reservation_data['ref'],
#             'channelNotes': reservation_data['channelNotes'],
#             'check in effettuato': reservation_data['effectiveCheckin'],
#             'check out effettuato': reservation_data['effectiveCheckout'],
#             'check out effettuato': reservation_data['effectiveCheckout']
#         }

#         changes = {}
#         for field, new_value in updated_data.items():
#             if field in field_labels and field in reservation_data:
#                 old_value = getattr(invoice_record, field, None)
#                 if new_value != old_value:
#                     formatted_new_value = new_value.strftime('%Y-%m-%d') if isinstance(new_value, datetime.date) else new_value
#                     changes[field] = formatted_new_value
#                     invoice_record.sudo().write({field: new_value})

#         booking_name = f"Prenotazione {reservation_data['refer']} dal {checkin_date} al {checkout_date}"
#         for line in invoice_record.invoice_line_ids:
#             if line.product_id.name == reservation_data['roomName']:
#                 line.write({'name': booking_name, 'price_unit': reservation_data['roomGross'], 'quantity': reservation_data['rooms']})
#             elif line.product_id.name == 'Tassa di Soggiorno':
#                 line.write({'quantity': reservation_data['totalGuest'] * num_notti, 'price_unit': 2})

#         if changes:
#             invoice_message_body = generate_message_body(reservation_data, field_labels, changes, is_update=True, include_chatter_fields=True)
#             invoice_record.message_post(body=invoice_message_body, message_type='comment')


# ***************************************CODICE SIMONE**********************************************************************************
#copyright © Simone Tullino 08/11

# VANGELO
# #{
#     "accessToken": "8720c548cbd14d1494371be717fca1ebSQYJOXLJAU",
#     "access_token": "8720c548cbd14d1494371be717fca1ebSQYJOXLJAU",
#     "expireDate": "2023-11-23T13:46:57.802Z[UTC]",
#     "refresh_token": "2acf003360ea4ebca6871b5d7e56efe2"
# }

# code=98a13ecebeab4e978beba9e9448105e73bc03fe8e7af4769a5a43ec6676912ba
import requests

from odoo import http, fields
from odoo.http import request, Response, _logger
from odoo.tools.safe_eval import json, datetime
import json
import requests
from datetime import datetime

CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"
ACCESS_TOKEN_POSTMAN=  "8720c548cbd14d1494371be717fca1ebSQYJOXLJAU"

def refresh_access_token():
    url = "https://api.octorate.com/connect/rest/v1/identity/refresh"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': '2acf003360ea4ebca6871b5d7e56efe2'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        _logger.error(f"Errore nella generazione del nuovo access token: {response.status_code} - {response.text}")
        return None



def fetch_octorate_reservations(accommodation_id, start_date, access_token):
    url = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {
        'Authorization': f'Bearer {access_token}', 
        'Content-Type': 'application/json'
    }
    # Inserimento manuale dell'access token di sopra
    params = {
        'type': 'CHECKIN',
        'startDate': start_date.strftime("%Y-%m-%d")
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()  # O la struttura dati appropriata
    # elif response.status_code == 401: 
    #     new_access_token = refresh_access_token()
    #     if new_access_token:
    #         return fetch_octorate_reservations(accommodation_id, start_date, access_token)
    #     else:
    #         return []
    else:
        new_access_token = refresh_access_token()
        if new_access_token:
            return fetch_octorate_reservations(accommodation_id, start_date, access_token)
        else:
            _logger.error(f"Errore nel recupero delle prenotazioni: {response.status_code} - {response.text}")
            return []

    # else:
    #     _logger.error(f"Errore nel recupero delle prenotazioni: {response.status_code} - {response.text}")
    #     return []



def fetch_room_cleaning_details(pms_product_id, access_token):
    url = "https://api.octorate.com/connect/rest/v1/pms"
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("data", [])
        for room in data:
            if room["id"] == pms_product_id:
                return room.get("clean"), room.get("lastCleaningDate"), room.get("name")
    else:
        new_access_token = refresh_access_token()  # Usa il tuo refresh token qui
        if new_access_token:
            return fetch_room_cleaning_details(pms_product_id, access_token)
        else:
            _logger.error(f"Errore nella richiesta dei dettagli della pulizia della stanza: {response.status_code} - {response.text}")
            return None, None, None     
    # elif response.status_code == 401:  # Token scaduto o non valido
    #     new_access_token = refresh_access_token()  # Usa il tuo refresh token qui
    #     if new_access_token:
    #         return fetch_room_cleaning_details(pms_product_id, access_token)
    #     else:
    #         return None, None, None



class RoomBookingController(http.Controller):
    @http.route('/api/prova', cors='*', auth='public', methods=['POST'], csrf=False, website=False)

   
    def handle_custom_endpoint(self, **post):
        try:
            # Recupera le prenotazioni da Octorate
            reservations_response = fetch_octorate_reservations(112696, datetime(2023, 12, 1), access_token= ACCESS_TOKEN_POSTMAN )
            # reservations = fetch_octorate_reservations(112696, datetime(2023, 12, 1))
            print(f"Le prenotazioni dell'istanza di produzione sono", reservations_response)
            reservations = reservations_response.get("data", [])

            # json_data = request.httprequest.data
            # print(f"Il print del json data è", json_data)
            # data_dict = json.loads(json_data)
            # print(f"Il json sottoforma di dizionario è", data_dict)
            # reservation = json.loads(data_dict.get("data"))
            # print(f"Le prenotazioni dell'istanza di produzione sono", reservation)

            for reservation in reservations:
                # Esempio di estrazione dei dati da una prenotazione
                refer_ = reservation.get("refer")
                guestsList_ = reservation.get("guestsList")
                roomGross_ = reservation.get("roomGross")
                totalGuest_ = reservation.get("totalGuest")
                numero_stanza_ = reservation.get("rooms")
                # priceBreakdown = reservation.get("priceBreakdown")
                # prezzo_unitario_ = priceBreakdown[0].get("price")
                data_creazione_ = reservation.get("createTime")
                note_interne_= reservation.get("channelNotes")
                # **info cliente**
                guests = reservation.get("guests")
                checkin_ = guests[0].get("checkin")
                checkout_ = guests[0].get("checkout")
                city_ = guests[0].get("city")
                email_ = guests[0].get("email")
                phone_ = guests[0].get("phone")
                address_ = guests[0].get("address")
                # effettivo_Checkin = reservation.get("effectiveCheckin")
                # effettivo_Checkout = reservation.get("effectiveCheckout")
                tipo_pagamento = reservation.get("paymentType")
                stato_pagamento = reservation.get("paymentStatus")

                checkin_date = fields.Date.from_string(checkin_)
                checkout_date = fields.Date.from_string(checkout_)
                data_creazione_mod = fields.Date.from_string(data_creazione_)
                delta = checkout_date - checkin_date
                n_notti = delta.days
                quantity_soggiorno = totalGuest_ * n_notti
                piattaforma = reservation.get("channelName")
                # Da domani partire da QUA
                clean, last_cleaning_date, name = fetch_room_cleaning_details(pms_product_id=57594, access_token=ACCESS_TOKEN_POSTMAN)

                # Controlla se la prenotazione esiste già in Odoo
                existing_invoice = request.env['account.move'].sudo().search([('refer', '=', refer_), ('move_type', '=', 'out_invoice')], limit=1)
                if not existing_invoice:
                    # La prenotazione non esiste, quindi creala
                    contact_bb = request.env['res.partner'].sudo().create({
                        # 'company_type': 'person',
                        # 'name': guestsList_,
                        "refer": refer_,
                        "prezzo totale": roomGross_,
                        "ospiti": totalGuest_,
                        "checkin": checkin_,
                        "checkout": checkout_,
                        "numero stanza": numero_stanza_,
                        "numero notti": n_notti,
                        "quantity_soggiorno": quantity_soggiorno,
                        # "prezzo unitario": prezzo_unitario_,
                        "city_utente": city_,
                        "email": email_,
                        "guestsList": guestsList_,
                        "telefono": phone_,
                        "indirizzo": address_,
                        "tipo": tipo,
                        "nome stanza" : nome_stanza,
                        "creazione fattura" : data_creazione_,
                        "nota Interna": note_interne_,
                        #"Tipologia prodotto id": psm,
                        #"Tipologia camera": room_name,
                        "Piattaforma di prenotazione": piattaforma,
                        # "Checkin effettuato": effettivo_Checkin,
                        # "Checkout effettuato": effettivo_Checkout,
                        "Tipo pagamento": tipo_pagamento,
                        "Stato pagamento": stato_pagamento,
                        "Stato camera": 'Clean' if clean else 'Not Clean',
                        "Ultima pulizia": last_cleaning_date,
                        "Tipologia camera": name
                    })

                    contact_id = contact_bb.id
                    _logger.info(f"ID CONTATTO CREATO : {contact_id}")

                        # Creazione della prenotazione (fattura)
                        # room_booking_obj = request.env['account.move'].sudo().create({
                        #     # ... Campi della fattura ...
                        # })

                    room_booking_obj = request.env['account.move'].sudo().create({
                        'state': 'draft',
                        'journal_id': customer_invoice_journal.id,
                        'refer': refer_,
                        'move_type': 'out_invoice',
                        'checkin': checkin_,
                        'checkout': checkout_,
                        'totalGuest': totalGuest_,
                        'rooms': n_notti,
                        'roomGross': roomGross_,
                        'partner_id': intero_contact,
                        'invoice_date': data_creazione_mod,
                        #'ref': room_name,
                        'team_id': team_vendite.id,
                        'email_utente': email_,
                        'telefono_utente': phone_,
                        'nome_stanza_utente': nome_stanza,
                        'nota_interna': note_interne_,
                        'checkin_effettuato': effettivo_Checkin,
                        'checkout_effettuato': effettivo_Checkout,
                        'stato_del_pagamento': stato_pagamento,
                        'tipo_di_pagamento': tipo_pagamento,
                        'pulizia_camera': clean,
                        'ultima_pulizia': last_cleaning_date,
                        'tipologia_camera': name,

                    })

                    # Creazione delle linee della fattura
                    linee_fattura = []
                    # Aggiungi qui le linee della fattura
                    
                # Linea per il prodotto 1 (Pernotto)
                    linea_fattura_pernotto = {
                        'move_id': room_booking_obj.id,
                        'product_id': room_product.id,
                        'name': f"Prenotazione {refer_} dal {checkin_} al {checkout_}",
                        'quantity': 1,
                        'price_unit': roomGross_,
                        'account_id': customer_account.id
                    }
                    linee_fattura.append(linea_fattura_pernotto)

                    # Linea per il prodotto 2 (Tassa di Soggiorno)
                    linea_fattura_tassasoggiorno = {
                        'move_id': room_booking_obj.id,
                        'product_id': tassa_soggiorno.id,
                        'name': "Tassa di soggiorno",
                        'quantity': quantity_soggiorno,
                        'account_id': customer_account.id
                    }
                    linee_fattura.append(linea_fattura_tassasoggiorno)

                    for line in linee_fattura:
                        request.env['account.move.line'].sudo().create(line)

                    # Aggiornamento dello stato della fattura e invio di un messaggio
                    room_booking_obj.with_context(default_type='out_invoice').write({'state': 'draft'})
                    room_booking_obj.message_post(
                    body=f"<p><b><font size='4' face='Arial'>Riepilogo dei dati:</font></b><br>"
                            f"Refer: {refer_}<br>"
                            f"Prezzo totale: {roomGross_}<br>"
                            f"Ospiti: {totalGuest_}<br>"
                            f"Checkin: {checkin_}<br>"
                            f"Checkout: {checkout_}<br>"
                            f"Numero stanza: {numero_stanza_}<br>"
                            f"Numero notti: {n_notti}<br>"
                            f"Quantity soggiorno: {quantity_soggiorno}<br>"
                            f"Prezzo unitario: {prezzo_unitario_}<br>"
                            f"City utente: {city_}<br>"
                            f"Email: {email_}<br>"
                            f"Guests List: {guestsList_}<br>"
                            f"Telefono: {phone_}<br>"
                            f"Indirizzo: {address_}<br>"
                            f"<span style='color:red; font-weight:bold;'>Note interne: {note_interne_}</span><br>"
                            f"Nome stanza: {nome_stanza}<br>"
                            f"Nome camera: {name}<br>"
                            f"Pulizia camera:{clean}<br>"
                            f"Ultima pulizia:{last_cleaning_date}<br>"
                            f"Piattaforma di prenotazione: {piattaforma}<br>"
                            f"Check in effettuato: {effettivo_Checkin} <br>"
                            f"Check out effettuato: {effettivo_Checkout} <br>"
                            f"Stato del pagamento: {stato_pagamento} <br>"
                            f"Tipo di pagamento: {tipo_pagamento} </pr>",
                    message_type='comment'
                )

            # ... (il resto del tuo codice esistente) ...

        
            json_data = request.httprequest.data
            data_dict = json.loads(json_data)
            _logger.info(f"Received data: {data_dict}")

            if 'ping' in data_dict:
                _logger.info("Ping received")
                return Response("Pong", content_type='text/plain', status=200)

            content = json.loads(data_dict.get("content"))
            

            # Estrai il valore del campo 'checkin' dal dizionario dei dati
            refer_ = content.get("refer")
            guestsList_ = content.get("guestsList")
            roomGross_ = content.get("roomGross")
            totalGuest_ = content.get("totalGuest")
            numero_stanza_ = content.get("rooms")
            priceBreakdown = content.get("priceBreakdown")
            prezzo_unitario_ = priceBreakdown[0].get("price")
            data_creazione_ = content.get("createTime")
            note_interne_= content.get("channelNotes")
            # **info cliente**
            guests = content.get("guests")
            checkin_ = guests[0].get("checkin")
            checkout_ = guests[0].get("checkout")
            city_ = guests[0].get("city")
            email_ = guests[0].get("email")
            phone_ = guests[0].get("phone")
            address_ = guests[0].get("address")
            effettivo_Checkin = content.get("effectiveCheckin")
            effettivo_Checkout = content.get("effectiveCheckout")
            tipo_pagamento = content.get("paymentType")
            stato_pagamento = content.get("paymentStatus")

            tipo = data_dict.get('type')

            #gestione della tipologia della camera
            # psm = content.get("pmsProduct")
            # id_to_room_name = {
            #     "599451": "Sky 001 Real Room",
            #     "599455": "Los Angeles Apartment 101",
            #     "612859": "quadrupla sepa"
            #     # Aggiungi altre associazioni ID-nome qui secondo necessità
            # }
            # room_name = id_to_room_name.get(str(psm))
            #piattaforma di prenotazione
            piattaforma = content.get("channelName")

            checkin_date = fields.Date.from_string(checkin_)
            checkout_date = fields.Date.from_string(checkout_)
            data_creazione_mod = fields.Date.from_string(data_creazione_)
            delta = checkout_date - checkin_date
            n_notti = delta.days
            quantity_soggiorno = totalGuest_ * n_notti
            nome_stanza = content.get("roomName")
            

            # gestione della tipologia della camera
            pms_product_id = content.get("pmsProduct")
            clean, last_cleaning_date, name = fetch_room_cleaning_details(pms_product_id, access_token=ACCESS_TOKEN_POSTMAN)


            response_data = {
                "refer": refer_,
                "prezzo totale": roomGross_,
                "ospiti": totalGuest_,
                "checkin": checkin_,
                "checkout": checkout_,
                "numero stanza": numero_stanza_,
                "numero notti": n_notti,
                "quantity_soggiorno": quantity_soggiorno,
                "prezzo unitario": prezzo_unitario_,
                "city_utente": city_,
                "email": email_,
                "guestsList": guestsList_,
                "telefono": phone_,
                "indirizzo": address_,
                "tipo": tipo,
                "nome stanza" : nome_stanza,
                "creazione fattura" : data_creazione_,
                "nota Interna": note_interne_,
                #"Tipologia prodotto id": psm,
                #"Tipologia camera": room_name,
                "Piattaforma di prenotazione": piattaforma,
                "Checkin effettuato": effettivo_Checkin,
                "Checkout effettuato": effettivo_Checkout,
                "Tipo pagamento": tipo_pagamento,
                "Stato pagamento": stato_pagamento,
                "Stato camera": 'Clean' if clean else 'Not Clean',
                "Ultima pulizia": last_cleaning_date,
                "Tipologia camera": name
            }
            #creazione piattaforma

            team_vendite = request.env['crm.team'].sudo().search([('name','=',piattaforma)], limit=1)
            if not team_vendite:
                team_vendite = request.env['crm.team'].sudo().create({'name': piattaforma})

            # Creazione della fattura
            room_booking_obj = []  # Inizializza la variabile come False
            customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
            customer_account = request.env['account.account'].sudo().search([('name', '=', 'Merci c/vendite')], limit=1)
            room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)], limit=1)
            if not room_product:
                room_product = request.env['product.product'].sudo().create({'name': nome_stanza})
            tassa_soggiorno = request.env['product.product'].sudo().search([('name', '=', "Tassa soggiorno")], limit=1)

            if tipo == 'RESERVATION_CREATED':
                # ********CONTROLLO/CREAZIONE DEL CONTATTO******
                contact_bb = request.env['res.partner'].sudo().create({
                    'company_type': 'person',
                    'name': guestsList_,
                    'street': address_,
                    'city': city_,
                    'email': email_,
                    'phone': phone_
                })

                # stampa l'ID del contatto appena creato
                contact_id = contact_bb.id
                intero_contact = int(contact_id)
                print("ID CONTATTO CREATO : ", intero_contact)



                room_booking_obj = request.env['account.move'].sudo().create({
                    'state': 'draft',
                    'journal_id': customer_invoice_journal.id,
                    'refer': refer_,
                    'move_type': 'out_invoice',
                    'checkin': checkin_,
                    'checkout': checkout_,
                    'totalGuest': totalGuest_,
                    'rooms': n_notti,
                    'roomGross': roomGross_,
                    'partner_id': intero_contact,  # Utilizza l'ID del contatto come partner_id
                    'invoice_date': data_creazione_mod,
                    #'ref': room_name,
                    'team_id': team_vendite.id,
                    'email_utente': email_,
                    'telefono_utente': phone_,
                    'nome_stanza_utente': nome_stanza,
                    'nota_interna': note_interne_,
                    'checkin_effettuato': effettivo_Checkin,
                    'checkout_effettuato': effettivo_Checkout,
                    'stato_del_pagamento': stato_pagamento,
                    'tipo_di_pagamento': tipo_pagamento,
                    'pulizia_camera': clean,
                    'ultima_pulizia': last_cleaning_date,
                    'tipologia_camera': name,

                })

                # Creazione delle linee della fattura
                linee_fattura = []

                # Linea per il prodotto 1 (Pernotto)
                linea_fattura_pernotto = {
                    'move_id': room_booking_obj.id,
                    'product_id': room_product.id,  # ID del prodotto 'Pernotto' nel portale amministrazione
                    'name': f"Prenotazione {refer_} dal {checkin_} al {checkout_}",
                    'quantity': 1,
                    'price_unit': roomGross_,
                    'account_id': customer_account.id
                }
                linee_fattura.append(linea_fattura_pernotto)

                # Linea per il prodotto 2 (Tassa di Soggiorno)
                linea_fattura_tassasoggiorno = {
                    'move_id': room_booking_obj.id,
                    'product_id': tassa_soggiorno.id,  # ID del prodotto 'Tassa di Soggiorno' nel portale amministrazione
                    'name': "Tassa di soggiorno",
                    'quantity': quantity_soggiorno,
                    'account_id': customer_account.id
                }
                linee_fattura.append(linea_fattura_tassasoggiorno)
                for line in linee_fattura:
                    request.env['account.move.line'].sudo().create(line)

                room_booking_obj.with_context(default_type='out_invoice').write({'state': 'draft'})
                room_booking_obj.message_post(
                    body=f"<p><b><font size='4' face='Arial'>Riepilogo dei dati:</font></b><br>"
                         f"Refer: {refer_}<br>"
                         f"Prezzo totale: {roomGross_}<br>"
                         f"Ospiti: {totalGuest_}<br>"
                         f"Checkin: {checkin_}<br>"
                         f"Checkout: {checkout_}<br>"
                         f"Numero stanza: {numero_stanza_}<br>"
                         f"Numero notti: {n_notti}<br>"
                         f"Quantity soggiorno: {quantity_soggiorno}<br>"
                         f"Prezzo unitario: {prezzo_unitario_}<br>"
                         f"City utente: {city_}<br>"
                         f"Email: {email_}<br>"
                         f"Guests List: {guestsList_}<br>"
                         f"Telefono: {phone_}<br>"
                         f"Indirizzo: {address_}<br>"
                         f"<span style='color:red; font-weight:bold;'>Note interne: {note_interne_}</span><br>"
                         f"Nome stanza: {nome_stanza}<br>"
                         f"Nome camera: {name}<br>"
                         f"Pulizia camera:{clean}<br>"
                         f"Ultima pulizia:{last_cleaning_date}<br>"
                         f"Piattaforma di prenotazione: {piattaforma}<br>"
                         f"Check in effettuato: {effettivo_Checkin} <br>"
                         f"Check out effettuato: {effettivo_Checkout} <br>"
                         f"Stato del pagamento: {stato_pagamento} <br>"
                         f"Tipo di pagamento: {tipo_pagamento} </pr>",
                    message_type='comment'
                )


            # ***********************************# PRENOTAZIONE MODIFICATA**************************************************
            elif tipo == 'RESERVATION_CHANGE':

                existing_invoice = request.env['account.move'].sudo().search([

                    ('refer', '=', refer_),

                    ('move_type', '=', 'out_invoice')

                ], limit=1)

                if existing_invoice:
                    existing_invoice.write({
                        'state': 'draft',
                        'journal_id': customer_invoice_journal.id,
                        'refer': refer_,
                        'move_type': 'out_invoice',
                        'checkin': checkin_,
                        'checkout': checkout_,
                        'totalGuest': totalGuest_,
                        'roomGross': roomGross_,
                        'invoice_date': data_creazione_mod,  # DOMANDA:  DEVO AGGIUNGERE LA DATA DI MODIFICA?
                        # 'partner_id': intero_contact  # Utilizza l'ID del contatto come partner_id
                        #'ref': room_name,
                        'team_id': team_vendite.id,
                        'email_utente': email_,
                        'telefono_utente': phone_,
                        'nome_stanza_utente': nome_stanza,
                        'tipologia_camera': name,
                        'pulizia_camera': clean,
                        'ultima_pulizia': last_cleaning_date,
                        'nota_interna': note_interne_,
                        'checkin_effettuato': effettivo_Checkin,
                        'checkout_effettuato': effettivo_Checkout,
                        'stato_del_pagamento': stato_pagamento,
                        'tipo_di_pagamento': tipo_pagamento
                    })

                    existing_invoice_line_ids = existing_invoice.invoice_line_ids

                    # Modifica le linee di fattura esistenti
                    for line in existing_invoice_line_ids:
                        if line.product_id.id == room_product.id:  # ID del prodotto 'Pernotto'
                            # Aggiorna le informazioni relative al prodotto 'Pernotto'
                            line.write({
                                'name': f"Prenotazione {refer_} dal {checkin_} al {checkout_}",
                                'quantity': 1,
                                'price_unit': roomGross_
                                # Aggiungi altri campi da aggiornare
                            })
                        elif line.product_id.id == tassa_soggiorno.id:  # ID del prodotto 'Tassa di Soggiorno'
                            # Aggiorna le informazioni relative al prodotto 'Tassa di Soggiorno'
                            line.write({
                                'name': "Tassa di soggiorno",
                                'quantity': quantity_soggiorno
                                # Aggiungi altri campi da aggiornare
                            })

                room_booking_obj = existing_invoice






            # **************************************# PRENOTAZIONE CANCELLATA**********************************************************************************************


            elif tipo == 'RESERVATION_CANCELLED':

                # Cerca la fattura esistente basata su 'refer' e 'move_type'

                existing_invoice = request.env['account.move'].sudo().search([

                    ('refer', '=', refer_),

                    ('move_type', '=', 'out_invoice')

                ], limit=1)

                if existing_invoice:
                    # Imposta lo stato della fattura esistente a 'cancel'

                    existing_invoice.write({

                        'state': 'cancel'

                    })

                    # Assegna la fattura esistente all'oggetto room_booking_obj

                    room_booking_obj = existing_invoice


            print("La fattura ha il seguyente id ---------->", room_booking_obj.id)

            # room_booking_obj.action_post()
            print("postata")
            return Response(json.dumps(response_data), content_type='application/json')
        except json.JSONDecodeError as e:
            _logger.error(f"JSON Decode Error: {e}")
            return Response("Invalid JSON format", content_type='text/plain', status=400)
        except Exception as e:
            _logger.exception("An unexpected error occurred")
            return Response("Internal Server Error", content_type='text/plain', status=500)



# SECONDA PARTE

# # Utilizzo della funzione
# reservations = fetch_octorate_reservations(access_token, 112696, datetime(2023, 12, 1))
# # Segue la logica per gestire queste prenotazioni


# try:
#     from json.decoder import JSONDecodeError
# except ImportError:
#     JSONDecodeError = ValueError
#*****************************************prova*****************
#https://odoo16-prenotazione-bb.unitivastaging.it/api/prova

#*********************route****************************

# checkin_str = content.get("guests")[0].get("checkin")
#             checkout_str = content.get("guests")[0].get("checkout")
            
#             try:
#                 checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
#                 checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
#             except ValueError:
#                 return Response("Invalid date format", content_type='text/plain', status=400)
            
#             start_validity_date = datetime.datetime(2024, 1, 1).date()
#             end_validity_date = datetime.datetime(2024, 1, 1).date()
#             if checkin_date and checkin_date < start_validity_date:
#                 _logger.info(f"Il checkin per la data seguente: {checkin_date} è stato ignorato")
#                 return Response("Check in ignorato", content_type='text/plain', status=200)
#             elif checkout_date and checkout_date < end_validity_date:
#                 _logger.info(f"Il checkout per la data seguente: {checkout_date} è stato ignorato")
#                 return Response("Check out ignorato", content_type='text/plain', status=200)




# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

# def get_access_token():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     payload = {
#         "grant_type": "authorization_code",
#         "code": "7042737ef65449ce829b4015de23239b1574276a6b6c4949a95d67df6cc4c497",
#         "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#         "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#         "redirect_uri": "https://localhost/"
#         # "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#     }

#     response = requests.post(endpoint, data=payload, headers=headers)

#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None
# # Ottieni il token di accesso
# access_token = get_access_token()

# if access_token:
#     print(f"Token per visionare le reservation è : {access_token}")
# else:
#     print("Errore nell'ottenere il token di accesso.")

