
# *****************************NEW CODE: TENTATIVO DI CORRISPONDENZA TRA IL NOME DEI CAMPI CREATI CON QUELLI AGGIORNATI NEL CHATTER ***************
from odoo import http, models
from odoo import _
from odoo.http import request, Response
import json
import datetime
import requests
import logging

CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"


# _logger = logging.getLogger(__name__)


field_labels = {
    'checkin': 'Checkin',
    'checkout': 'Checkout',
    'totalGuest': 'Numero totale ospiti',
    'totalChildren': 'Totale Bambini',
    'totalInfants': 'Totale Neonati',
    'rooms': 'Numero camere',
    'roomGross': 'Prezzo Unitario',
    'roomName': 'Nome Stanza',
    'ref': 'Riferimento',
    'channelNotes': 'Note aggiuntive',
    'partner_id': 'ID Cliente',
    'email': 'Email Cliente',
    'piattaforma': 'Piattaforma di Prenotazione',
    'invoicedate': 'Data Fattura',
    'pmsProduct': 'Prodotto PMS',
    'PaymentStatus': 'Stato del pagamento',
    'PaymentType': 'Tipo di pagamento',
    'effectiveCheckin': 'Check in effettuato',
    'effectiveCheckout': 'Check out effettuato',
    'privateNotes': 'Note interne'
}

def generate_message_body(data, field_labels, is_update=False, include_chatter_fields=False):
    lines = []
    for field, label in field_labels.items():
        if field in data and (include_chatter_fields or field not in ['privateNotes', 'effectiveCheckin', 'effectiveCheckout']):
            value = data[field]
            formatted_value = value.strftime('%Y-%m-%d') if isinstance(value, datetime.date) else value
            lines.append(f"{label}: {formatted_value}")

    if is_update:
        title = "Dati aggiornati:"
    else:
        title = "Dati di fatturazione creati:"

    return f"<p><b><font size='4' face='Arial'>{title}</font></b><br>" + "<br>".join(lines) + "</p>"
_logger = logging.getLogger(__name__)

def fetch_room_cleaning_details(pms_product_id):
    url = "https://api.octorate.com/connect/rest/v1/pms"
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 5fc9e202a3ce46c592bb793b3a70a6adHRGYUDTYFO'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("data", [])
        for room in data:
            if room["id"] == pms_product_id:
                _logger.info(f"Room data found: {room}")
                return room.get("clean"), room.get("lastCleaningDate"), room.get("name")
            else:
                _logger.info(f"Room data not matching: {room}")
    else:
        _logger.error(f"Failed to fetch room details: {response.status_code} - {response.text}")
    return None, None, None


# def fetch_room_cleaning_details(pms_product_id):
#     url = "https://api.octorate.com/connect/rest/v1/pms"
#     # Usa il token statico qui
#     headers = {
#         'accept': 'application/json',
#         'Authorization': 'Bearer 00c892e4b305483fbe74bbf1fb3dcf18QWFVRTEFIP'
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json().get("data", [])
#         for room in data:
#             if room["id"] == pms_product_id:
#                 return room.get("clean"), room.get("lastCleaningDate"), room.get("name")
#     return None, None, None




class RoomBookingController(http.Controller):

    @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
    def handle_custom_endpoint(self, **post):
        json_data = request.httprequest.data
        data_dict = json.loads(json_data)
        content = json.loads(data_dict.get("content"))
        create_time_str = data_dict.get("createTime")

        try:
            create_time = datetime.datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%SZ[UTC]') if create_time_str else None
        except ValueError:
            return Response("Invalid date format for createTime", content_type='text/plain', status=400)

        if not content.get("refer") or not content.get("guests"):
            return Response("Missing required fields", content_type='text/plain', status=400)

        checkin_str = content.get("guests")[0].get("checkin")
        checkout_str = content.get("guests")[0].get("checkout")
        
        try:
            checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
            checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
        except ValueError:
            return Response("Invalid date format", content_type='text/plain', status=400)

        reservation_data = {
            'partner_id': content.get("guestsList"),
            'email': content.get("guestMailAddress"),
            'refer': content.get("refer"),
            'ref': content.get('pmsProduct'),
            'roomName': content.get('roomName'),
            'checkin': checkin_date,
            'checkout': checkout_date,
            'channelNotes': content.get("channelNotes"),
            'totalGuest': content.get("totalGuest"),
            'totalChildren': content.get("totalChildren"),
            'totalInfants': content.get("totalInfants"),
            'rooms': content.get("rooms"),
            'roomGross': content.get("roomGross"),
            'invoicedate': create_time,
            'piattaforma': content.get("channelName"),
            'effectiveCheckin':content.get("effectiveCheckin"),
            'effectiveCheckout':content.get("effectiveCheckout"), 
            'note interne':content.get("privateNotes"),
            'Stato del pagamento':content.get("PaymentStatus"), 
            'Tipo di pagamento':content.get("PaymentType")
        }
        
        
        event_type = data_dict.get("type")
        response_data = {}

        if event_type == "RESERVATION_CREATED":
            invoice_details = self.calculate_invoice_details(reservation_data)
            self.create_invoice(reservation_data, invoice_details)
            response_data.update(invoice_details)
            
            
        elif event_type == "RESERVATION_CHANGE":
            refer_id = reservation_data.get('refer')
            nome_cliente=reservation_data.get('partner_id')

            invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id), ('partner_id', '=', nome_cliente)], limit=1)
            if not invoice_record:
                return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
            reservation_data.pop('email', None)
            if 'email' in request.env['account.move']._fields:
                invoice_record.sudo().write({'email': content.get("guestMailAddress")})
            # Aggiungi il messaggio di pulizia solo se invoice_record è stato definito
            if invoice_record:
                pms_product_id = content.get("pmsProduct")
                clean, last_cleaning_date, name = fetch_room_cleaning_details(pms_product_id)
                cleaning_details_message = f"Room Cleaning Status: {'Clean' if clean else 'Not Clean'}\n" \
                                        f"Last Cleaning Date: {last_cleaning_date}"\
                                        f"Nome specifico stanza: {name}"
                
                invoice_record.message_post(body=cleaning_details_message, message_type='comment')
                cleaning_details = {
                    'cleaning_status': 'Clean' if clean else 'Not Clean',
                    'last_cleaning_date': last_cleaning_date,
                    'name': name
                }
                response_data.update({'cleaning_details': cleaning_details})
# LALALA
            

            self.update_invoice_lines(invoice_record, reservation_data)
            response_data.update({
                "partner_id": invoice_record.partner_id.name,
                "move_id": invoice_record.id,
                "checkin": invoice_record.checkin.strftime('%Y-%m-%d') if isinstance(invoice_record.checkin, datetime.date) else invoice_record.checkin,
                "checkout": invoice_record.checkout.strftime('%Y-%m-%d') if isinstance(invoice_record.checkout, datetime.date) else invoice_record.checkout,
                "invoice_date": invoice_record.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(invoice_record.invoice_date, datetime.datetime) else invoice_record.invoice_date,
                "totalGuest": invoice_record.totalGuest,
                "totalChildren": invoice_record.totalChildren,
                "totalInfants": invoice_record.totalInfants,
                "rooms": invoice_record.rooms,
                "product_id": invoice_record.roomName,
                "note aggiuntive": invoice_record.channelNotes,
                "ref":invoice_record.pmsProduct,
                "state": invoice_record.state,
                "Piattaforma di prenotazione" : reservation_data["piattaforma"],
                "Checkin_effettuato" : reservation_data["effectiveCheckin"],
                "Checkout_effettuato" : reservation_data["effectiveCheckout"],
                "Note interne" : reservation_data["note interne"],
                'cleaning_details': cleaning_details
            })
            # 'effectiveCheckin':content.get("effectiveCheckin"),
            # 'effectiveCheckout':content.get("effectiveCheckout"), 
            # 'note interne':content.get("privateNotes"),
            # 'Stato del pagamento':content.get("PaymentStatus"), 
            # 'Tipo di pagamento':content.get("PaymentType")

        elif event_type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
            refer_id = reservation_data.get('refer')
            checkout_id=reservation_data.get('checkout')
            
            invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
            if not invoice_record:
                return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)

            if invoice_record.checkout != checkout_id:
                return Response(f"Invoice found with refer: {refer_id}, but with different checkout date.", content_type='text/plain', status=400)

            new_state = 'cancel' if event_type == 'RESERVATION_CANCELLED' else 'posted'
            invoice_record.sudo().write({'state': new_state})
        else:
            return Response("Invalid event type", content_type='text/plain', status=400)
        
        for key, value in response_data.items():
            if isinstance(value, datetime.date):
                response_data[key] = value.strftime('%Y-%m-%d')

        return Response(json.dumps(response_data), content_type='application/json', status=200)

    def calculate_invoice_details(self, reservation_data):
        nome_ospite= reservation_data['partner_id']
        checkin_date = reservation_data['checkin']
        
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        num_ospiti = reservation_data['totalGuest']

        tourist_tax_quantity = num_notti * num_ospiti * 2
        
        booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
        booking_quantity = reservation_data['rooms']
        booking_price_unit = reservation_data['roomGross']
        nome_stanza = reservation_data['roomName']
    
        return {
            "Orario creazione prenotazione": reservation_data["invoicedate"].strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(reservation_data["invoicedate"], datetime.datetime) else reservation_data["invoicedate"],
            "Nome ospite": nome_ospite,
            "Valore tassa turistica": tourist_tax_quantity,
            "Identificativo della prenotazione": booking_name,
            "Numero stanze": booking_quantity,
            "Costo stanza": booking_price_unit,
            "Tipologia stanza": nome_stanza,
            "Numero identificativo Camera": reservation_data["ref"]
            
        }

    def create_invoice(self, reservation_data, invoice_details):
        tax_0_percent = None
        partner_name = reservation_data['partner_id']
        nome_stanza = reservation_data['roomName']
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        partner = request.env['res.partner'].sudo().with_context(partner_display='invoice_partner_display_name').search([('name', '=', partner_name)], limit=1)
        team_vendite = request.env['crm.team'].sudo().search([('name','=',reservation_data["piattaforma"])], limit=1)
        if not team_vendite:
            team_vendite = request.env['crm.team'].sudo().create({'name': reservation_data["piattaforma"]})

        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': partner_name,
                'email': reservation_data.get('email'),
                'customer_rank': 1
            })

        room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)])
        if not room_product:
            room_product = request.env['product.product'].sudo().create({'name': nome_stanza})
            
        tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
        if not tassa_soggiorno_product:
            tax_0_percent = request.env['account.tax'].sudo().search(
                [('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)],
                limit=1
            )
            if not tax_0_percent:
                raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
            
            vals = {
                'name': 'Tassa di Soggiorno',
                'type': 'service',
            }
            
            if tax_0_percent is not None:
                vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]

            tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)
        
        customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
        journal_id = customer_invoice_journal.id
        partner_values = {
            'name': reservation_data["partner_id"],
            'email': reservation_data["email"],
        }

        partner = request.env['res.partner'].sudo().create(partner_values)
        partner_display_name = partner.name_get()[0][1] if partner else "Nuovo Partner"
        
        invoice_values = {
            'journal_id': journal_id,
            'move_type': 'out_invoice',
            'ref': reservation_data['ref'],
            'partner_id': partner.id,
            'invoice_partner_display_name': partner_display_name,
            'checkin': reservation_data['checkin'],
            'checkout': reservation_data['checkout'],
            'refer': reservation_data['refer'],
            'totalGuest': reservation_data['totalGuest'],
            'totalChildren': reservation_data['totalChildren'],
            'rooms': reservation_data['rooms'],
            'roomGross': reservation_data['roomGross'],
            'invoice_date': reservation_data['invoicedate'],
            'channelNotes': reservation_data['channelNotes'],
            'team_id': team_vendite.id
        }
        invoice_record = request.env['account.move'].sudo().create(invoice_values)
        invoice_message_body = generate_message_body(reservation_data, field_labels, is_update=False, include_chatter_fields=True)
        invoice_record.message_post(body=invoice_message_body, message_type='comment')

        booking_line_values = {
            'move_id': invoice_record.id,
            'product_id': room_product.id,
            'name': invoice_details['Identificativo della prenotazione'],
            'quantity': reservation_data['rooms'],
            'price_unit': invoice_details['Costo stanza'],
            'account_id': account_id
        }
        request.env['account.move.line'].sudo().create(booking_line_values)

        tourist_tax_line_values = {
            'move_id': invoice_record.id,
            'product_id': tassa_soggiorno_product.id,
            'name': "Tassa soggiorno",
            'quantity': reservation_data['totalGuest']*num_notti,
            'price_unit': 2,
            'account_id': account_id
        }
        request.env['account.move.line'].sudo().create(tourist_tax_line_values)

    def update_invoice_lines(self, invoice_record, reservation_data):
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days

        updated_data = {
            'invoice_date': reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.datetime) else reservation_data['invoicedate'],
            'checkin': checkin_date,
            'checkout': checkout_date,
            'totalGuest': reservation_data['totalGuest'],
            'totalChildren': reservation_data['totalChildren'],
            'rooms': reservation_data['rooms'],
            'roomGross': reservation_data['roomGross'],
            'ref': reservation_data['ref'],
            'channelNotes': reservation_data['channelNotes'],
            'check in effettuato': reservation_data['effectiveCheckin'],
            'check out effettuato': reservation_data['effectiveCheckout'],
            'check out effettuato': reservation_data['effectiveCheckout']
        }

        changes = {}
        for field, new_value in updated_data.items():
            if field in field_labels and field in reservation_data:
                old_value = getattr(invoice_record, field, None)
                if new_value != old_value:
                    formatted_new_value = new_value.strftime('%Y-%m-%d') if isinstance(new_value, datetime.date) else new_value
                    changes[field] = formatted_new_value
                    invoice_record.sudo().write({field: new_value})

        booking_name = f"Prenotazione {reservation_data['refer']} dal {checkin_date} al {checkout_date}"
        for line in invoice_record.invoice_line_ids:
            if line.product_id.name == reservation_data['roomName']:
                line.write({'name': booking_name, 'price_unit': reservation_data['roomGross'], 'quantity': reservation_data['rooms']})
            elif line.product_id.name == 'Tassa di Soggiorno':
                line.write({'quantity': reservation_data['totalGuest'] * num_notti, 'price_unit': 2})

        if changes:
            invoice_message_body = generate_message_body(reservation_data, field_labels, is_update=True, include_chatter_fields=True)
            invoice_record.message_post(body=invoice_message_body, message_type='comment')
