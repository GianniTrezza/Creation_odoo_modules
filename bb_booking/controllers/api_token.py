from odoo import http
from odoo.http import request
import requests


CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

def get_access_token_basic():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    response = requests.post(endpoint, data=payload, headers=headers)
    return response.json().get("access_token", None)

def get_access_token_full():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": "17e8df5ab404470fa78955472b9d5fd51ca6ff39bc3b4e11b0a92a7a59d04c6a",
        "grant_type": "authorization_code",
        "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
    }
    response = requests.post(endpoint, data=payload, headers=headers)
    print(response.status_code)
    print(response.json())  
    return response.json().get("access_token", None)


def fetch_accommodations(token):
    endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def choose_accommodation(accommodations):
    print("Scegli un accommodation:")
    for index, accommodation in enumerate(accommodations, start=1):
        print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
    choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
    return accommodations[choice-1].get("id")
# PRELIEVO DELLE RESERVATIONS SENZA FILTRI
def fetch_reservations(token, accommodation_id):
    endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

access_token_basic = get_access_token_basic()
access_token_full = get_access_token_full()
print(f"Ecco il token con grant parziale:{access_token_basic}")
print(f"Ecco il token con grant completo:{access_token_full}")

accommodations = fetch_accommodations(access_token_basic)

accommodation_id = choose_accommodation(accommodations)

reservations = fetch_reservations(access_token_full, accommodation_id)
print(f"Ecco le prenotazioni relative a {accommodation_id}: {reservations}")


def fetch_webhooks(access_token_full):
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token_full}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
        return []

    return response.json()

webhook_url="https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
webhooks = fetch_webhooks(access_token_full)
print(f"Ecco una lista di possibili webhook:{webhooks}")

# QUESTO SNIPPET FUNZIONA NELL'INVIARE I DATI DI PRENOTAZIONE AL WEBHOOK, MA NON è INTEGRATO CON ODOO
# class RoomBookingController(http.Controller):

#     @http.route('/room_booking/webhook', type='json', auth='public', methods=['POST'])
#     def receive_data(self, **kw):
#         data = request.jsonrequest
#         event_type = data.get('type')
#         webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

#         headers = {
#             'Content-Type': 'application/json'
#         }

#         response_message = {"message": "Event not supported"}

#         if event_type == "RESERVATION_CREATED":
#             reservation = request.env['bb_booking.roombooking'].sudo().create({
#                 'refer': data.get('reservation_id'),
#                 'checkin': data.get('checkin'),
#                 'checkout': data.get('checkout'),
#                 'totalChildren': data.get('totalChildren'),
#                 'totalInfants': data.get('totalInfants'),
#                 'totalGuest': data.get('totalGuest'),
#                 'roomGross': data.get('roomGross'),
#                 'totalGross': data.get('totalGross'),
#             })

#             try:
#                 response = requests.post(webhook_url, json=data, headers=headers)
#                 if response.status_code == 200:
#                     response_message = {"message": "Reservation created and data sent to webhook"}
#                 else:
#                     response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#             except requests.RequestException as e:
#                 response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CANCELLED":
#             reservation_id = data.get('reservation_id')
#             # reservation = request.env['bb_booking.roombooking'].sudo().search([('id', '=', reservation_id)])
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 # reservation.write({'refer': 'Cancellato'})
#                 reservation.write({'status': 'Cancellato'})

#                 # Invia i dati al webhook
#                 try:
#                     response = requests.post(webhook_url, json=data, headers=headers)  # Qui includiamo gli headers
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation cancelled and data sent to webhook"}
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except requests.RequestException as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CONFIRMED":
#             reservation_id = data.get('reservation_id')
#             # reservation = request.env['bb_booking.roombooking'].sudo().search([('id', '=', reservation_id)])
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 # reservation.write({'refer': 'Confermato'})
#                 reservation.write({'status': 'Confermato'})

#                 try:
#                     response = requests.post(webhook_url, json=data, headers=headers)
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation confirmed and data sent to webhook"}
#                         print(response_message)
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except requests.RequestException as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         return response_message

# NEW ATTEMPT PER DOMANI (12/10/2023)
from odoo import http
from odoo.http import request
import requests

class RoomBookingController(http.Controller):

    @http.route('/reservation/webhook', type='json', auth='public', methods=['POST'])
    def receive_data(self, **kw):
        data = request.jsonrequest
        event_type = data.get('type')
        webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
        headers = {'Content-Type': 'application/json'}
        response_message = {"message": "Event not supported"}

        if event_type == "RESERVATION_CREATED":
            reservation = request.env['bb_booking.roombooking'].sudo().create({
                'refer': data.get('refer'),
                'checkin': data.get('checkin'),
                'checkout': data.get('checkout'),
                'totalChildren': data.get('totalChildren'),
                'totalInfants': data.get('totalInfants'),
                'totalGuest': data.get('totalGuest'),
                'roomGross': data.get('roomGross'),
                'totalGross': data.get('totalGross'),
            })

            try:
                response = requests.post(webhook_url, json=data, headers=headers)
                if response.status_code == 200:
                    response_message = {"message": "Reservation created and data sent to webhook"}
                else:
                    response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
            except requests.RequestException as e:
                response_message = {"message": f"Request failed: {str(e)}"}

        elif event_type == "RESERVATION_CANCELLED":
            reservation_id = data.get('reservation_id')
            reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

            if reservation:
                reservation.write({'status': 'Cancellato'})

                try:
                    response = requests.post(webhook_url, json=data, headers=headers)
                    if response.status_code == 200:
                        response_message = {"message": "Reservation cancelled and data sent to webhook"}
                    else:
                        response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
                except requests.RequestException as e:
                    response_message = {"message": f"Request failed: {str(e)}"}

        elif event_type == "RESERVATION_CONFIRMED":
            reservation_id = data.get('reservation_id')
            reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

            if reservation:
                reservation.write({'status': 'Confermato'})

                try:
                    response = requests.post(webhook_url, json=data, headers=headers)
                    if response.status_code == 200:
                        response_message = {"message": "Reservation confirmed and data sent to webhook"}
                    else:
                        response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
                except requests.RequestException as e:
                    response_message = {"message": f"Request failed: {str(e)}"}

        return response_message



# FUNZIONE CHE TI CONSENTE DI SCEGLIERE TRA GLI EVENTS COSICCHé TU POSSA MANDARE I DATI RELATIVI AL WEBHOOK CIASCUN EVENT ALLA VOLTA
# def choose_event():
#     EVENTS = [
#         "RESERVATION_CREATED", "RESERVATION_CHANGE", "RESERVATION_CANCELLED", "RESERVATION_CONFIRMED",
#         "CONTENT_NOTIFICATION", "CONTENT_PUSH", "PORTAL_SUBSCRIPTION_CALENDAR",
#         "XXX_NOT_USED_PORTAL_PROCESS_FAILED", "CHAT_MESSAGE_RECEIVED"
#     ]
#     print("Scegli un evento per configurare il webhook:")
#     for index, event in enumerate(EVENTS, start=1):
#         print(f"{index}. {event}")
#     choice = int(input("Inserisci il numero corrispondente all'evento: "))
#     return EVENTS[choice-1]

# webhook_url = "https://webhook.site/7562c12d-e21c-402c-8faa-b6c08e9e564d"

