import requests
import json
import os

import jwt
from datetime import datetime, timedelta

# Chiave segreta (ideale in una variabile d'ambiente)
secret_key = 'ff383914fe26d613ace3f52e7da13a670ee69a84'

# Payload con scadenza
payload = {
    'user_id': 3,
    'username': 'admin@admin.it',
    'ruolo': 'amministratore',
    'exp': datetime.utcnow() + timedelta(days=1)  # Token scade dopo 1 giorno
}

# Genera il token JWT
token = jwt.encode(payload, secret_key, algorithm='HS256')
print(token)


# # Dati del client per ottenere il token
# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"


# # Funzione per ottenere il token di accesso
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


# def get_access_token2():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     payload = {
#         "grant_type": "authorization_code",
#         "code": "1d49af00a14a4604ad3214c39654d4b5f18064a6923f4bdaba7d1c867b6234a3",
#         "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#         "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#         "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#     }

#     response = requests.post(endpoint, data=payload, headers=headers)

#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None


# # Ottieni il token di accesso
# access_token_a = get_access_token2()

# if access_token_a:
#     print(f"Token per visionare le reservation è : {access_token_a}")
# else:
#     print("Errore nell'ottenere il token di accesso.")


# def refresh_token():
#    endpoint = "https://api.octorate.com/connect/rest/v1/identity/refresh"

#    headers = {
#        "Accept": "application/json",
#        "Content-Type": "application/x-www-form-urlencoded"
#    }

#    payload = {
#                 "grant_type": "authorization_code",
#                 "code": "cc4a0b29064f4b36992e1203acdbf613eb0eda5cd36c43bab2c687820d4c8e79",
#                "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#                "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#                 "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html",
#                 'refresh_token': '2acf003360ea4ebca6871b5d7e56efe2'
#    }

#    response = requests.post(endpoint, data=payload, headers=headers)

#    if response.status_code == 200:
#        print("refresh avvenuto con successo")
#        return response.json().get("access_token")
#    else:
#        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#        return None


# def fetch_accommodations(token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
#     # print(token)

#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {token}"
#     }

#     response = requests.get(endpoint, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Errore nell'ottenere gli accommodation: {response.headers}, {headers}")
#         return []


# # Esempio di utilizzo:
# # Ottieni il token di accesso (già ottenuto precedentemente)
# access_token = get_access_token()
# # Ottenere gli accommodation
# accommodations = fetch_accommodations(access_token)
# if accommodations:
#     print(f"Gli accommodation ottenuti con successo: {accommodations}")
# else:
#     print("Nessun accommodation disponibile o errore nell'ottenimento.")


# def fetch_reservations_for_accommodation_id(access_token_a, accommodation_id):
#     reservation_endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {access_token_a}"
#     }
#     response = requests.get(reservation_endpoint, headers=headers)

#     if response.status_code == 200:
#         reservations = response.json()
#         return reservations
#     else:
#         print(
#             f"Errore nell'ottenere le prime prenotazioni per l'alloggio {accommodation_id}, {headers}, {response.status_code}, {response.text}")
#         return []


# # Esempio di utilizzo:
# # Ottieni il token di accesso (già ottenuto precedentemente)

# # access_token_a = get_access_token2()
# # print(access_token_a)
# # Inserisci l'ID dell'alloggio per cui desideri ottenere le prenotazioni
# accommodation_id = "632966"

# # Ottieni le prenotazioni per l'alloggio selezionato utilizzando il token ottenuto
# reservations = fetch_reservations_for_accommodation_id(access_token_a, accommodation_id)

# # Controlla se ci sono prenotazioni
# if reservations:
#     print(f"{accommodation_id}: {reservations}")

#     # Converti le prenotazioni in formato JSON
#     reservations_json = json.dumps(reservations)

#     # Definisci l'URL del webhook al quale inviare le prenotazioni
#     webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

#     # Invia i dati al webhook
#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.post(webhook_url, data=reservations_json, headers=headers)

#     # Verifica la risposta del webhook
#     if response.status_code == 200:
#         print("Dati inviati con successo al webhook.")
#     else:
#         print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")
# else:
#     print("Nessuna prenotazione disponibile o errore nell'ottenimento.")

# print(f"{accommodation_id}:{reservations}")



# def fetch_webhooks(access_token_a):
#     endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access_token_a}"
#     }

#     response = requests.get(endpoint, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
#         return []

#     return response.json()



#
# def create_subscription(event_type, access_token_a):
#     # URL per il tipo di evento specifico
#     subscription_url = f"https://api.octorate.com/connect/rest/v1/subscription/{event_type}"
#     print(subscription_url)
#     # URL dell'endpoint a cui verranno inviati i webhook
#    # endpoint_url = "https://webhook.site/7562c12d-e21c-402c-8faa-b6c08e9e564d"
#
#     # Crea il payload per la richiesta
#     payload = {
#         "endpoint": webhook_url,
#         #"type": "CONTENT_NOTIFICATION"
#     }
#     print(payload)
#     # Aggiungi l'intestazione di autorizzazione
#     headers = {
#         "Authorization": f"Bearer {access_token_a}",
#         "Content-Type": "application/json"
#     }
#     print(headers)
#     # Invia la richiesta per creare l'abbonamento
#     response = requests.post(subscription_url, json=payload, headers=headers)
#
#     if response.status_code == 200:
#         print(f"Abbonamento per {event_type} creato con successo.")
#     else:
#         print(f"Errore durante la creazione dell'abbonamento per {event_type}: {response.status_code} - {response.text}")
#
# # Assicurati di avere un access token valido
#
#
# # Definisci i tipi di eventi per i quali vuoi creare gli abbonamenti
# event_types = ["RESERVATION_CREATED", "RESERVATION_CHANGE", "RESERVATION_CANCELLED", "RESERVATION_CONFIRMED"]
#
# # Chiamare la funzione per ciascun tipo di evento
# for event_type in event_types:
#     create_subscription(event_type, access_token_a)
#     print("è andata")


# body=f"<p><b><font size='4' face='Arial'>Dati aggiornati:</font></b><br>"
#                          f"Refer: {refer_}<br>"
#                          f"Prezzo totale: {roomGross_}<br>"
#                          f"Ospiti: {totalGuest_}<br>"
#                          f"Checkin: {checkin_}<br>"
#                          f"Checkout: {checkout_}<br>"
#                          f"Numero stanza: {numero_stanza_}<br>"
#                          f"Numero notti: {n_notti}<br>"
#                          f"Quantity soggiorno: {quantity_soggiorno}<br>"
#                          f"Prezzo unitario: {prezzo_unitario_}<br>"
#                          f"City utente: {city_}<br>"
#                          f"Email: {email_}<br>"
#                          f"Guests List: {guestsList_}<br>"
#                          f"Telefono: {phone_}<br>"
#                          f"Indirizzo: {address_}<br>"
#                          f"Nome stanza: {nome_stanza}<br></p>",
#                     message_type='comment'
#                 )

# from odoo import http, models
# from odoo.http import request, Response
# import json
# import datetime
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
# }


# def generate_message_body(data, field_labels):
#     lines = []
#     for field, label in field_labels.items():
#         if field in data:
#             value = data[field]
#             formatted_value = value.strftime('%Y-%m-%d') if isinstance(value, datetime.date) else value
#             lines.append(f"{label}: {formatted_value}")
#     return "<p><b><font size='4' face='Arial'>Dati di fatturazione:</font></b><br>" + "<br>".join(lines) + "</p>"

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
#             'piattaforma': content.get("channelName")
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
#                 "Piattaforma di prenotazione" : reservation_data["piattaforma"]
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
#         invoice_message_body = generate_message_body(reservation_data, field_labels)
#         invoice_record.message_post(body=invoice_message_body, message_type='comment')
#         # invoice_record.message_post(
#         #     body=f"<p><b><font size='4' face='Arial'>Dati di fatturazione creati:</font></b><br>"
#         #         f"Nome Cliente: {reservation_data['partner_id']}<br>"
#         #         f"Refer: {reservation_data['refer']}<br>"
#         #         f"Data Fattura: {reservation_data['invoicedate']}<br>"
#         #         f"Checkin: {checkin_date}<br>"
#         #         f"Checkout: {checkout_date}<br>"
#         #         f"Nome stanza: {nome_stanza}<br></p>"
#         #         f"Note stanza aggiuntive: {reservation_data['channelNotes']}<br>"
#         #         f"Numero bambini: {reservation_data['totalChildren']}<br>"
#         #         f"Ospiti: {reservation_data['totalGuest']}<br>"
#         #         f"Prezzo unitario: {reservation_data['roomGross']}<br>"
#         #         f"Piattaforma di prenotazione: {reservation_data['piattaforma']}</p>",
#         #     message_type='comment'
#         # )

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
#         # checkin_date = reservation_data['checkin']
#         # checkout_date = reservation_data['checkout']
#         # checkin_date = reservation_data['checkin']
#         # checkout_date = reservation_data['checkout']
#         # total_guest = reservation_data['totalGuest']
#         # total_children = reservation_data['totalChildren']
#         # rooms = reservation_data['rooms']
#         # room_gross= reservation_data['roomGross']
#         # room_name_guest= reservation_data['ref']
#         # delta = checkout_date - checkin_date
#         # num_notti = delta.days
#         # formatted_invoice_date = reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.datetime) else reservation_data['invoicedate']
        
        
#         changes = {field: reservation_data[field] for field in field_labels if field in reservation_data}
#         invoice_message_body = generate_message_body(changes, field_labels)
#         invoice_record.message_post(body=invoice_message_body, message_type='comment')
       
