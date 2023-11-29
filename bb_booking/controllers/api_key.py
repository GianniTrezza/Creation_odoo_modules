import requests
import json
import os


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
# token = jwt.encode(payload, secret_key, algorithm='HS256')
# print(token)


#Dati del client per ottenere il token
CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

#
# # Funzione per ottenere il token di accesso
# def get_access_token():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
#
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#
#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }
#
#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None
#
#
# # Ottieni il token di accesso
# access_token = get_access_token()
# if access_token:
#     print(f"Token di accesso ottenuto con successo: {access_token}")
# else:
#     print("Errore nell'ottenere il token di accesso.")
#
#
# def get_access_token2():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"
#
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#
#     payload = {
#         "grant_type": "authorization_code",
#         "code": "3c7611558345463bb4f29455cccb99f54f9a179690584decb36987c167e29886",
#         "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#         "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#         "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#     }
#
#     response = requests.post(endpoint, data=payload, headers=headers)
#
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None
#
#
# # Ottieni il token di accesso
# access_token_a = get_access_token2()
#
# if access_token_a:
#     print(f"Token per visionare le reservation è : {access_token_a}")
# else:
#     print("Errore nell'ottenere il token di accesso.")
#
#
# def refresh_token():
#    endpoint = "https://api.octorate.com/connect/rest/v1/identity/refresh"
#
#    headers = {
#        "Accept": "application/json",
#        "Content-Type": "application/x-www-form-urlencoded"
#    }
#
#    payload = {
#                 "grant_type": "authorization_code",
#                 "code": "cc4a0b29064f4b36992e1203acdbf613eb0eda5cd36c43bab2c687820d4c8e79",
#                 "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#                 "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#                 "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html",
#                 'refresh_token': '2acf003360ea4ebca6871b5d7e56efe2'
#    }
#
#    response = requests.post(endpoint, data=payload, headers=headers)
#
#    if response.status_code == 200:
#        print("refresh avvenuto con successo")
#        return response.json().get("access_token")
#    else:
#        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#        return None
#
#
# def fetch_accommodations(token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
#     # print(token)
#
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
#
#     response = requests.get(endpoint, headers=headers)
#
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Errore nell'ottenere gli accommodation: {response.headers}, {headers}")
#         return []

#
# # Esempio di utilizzo:
# # Ottieni il token di accesso (già ottenuto precedentemente)
# access_token = get_access_token()
# # Ottenere gli accommodation
# accommodations = fetch_accommodations(access_token)
# if accommodations:
#     print(f"Gli accommodation ottenuti con successo: {accommodations}")
# else:
#     print("Nessun accommodation disponibile o errore nell'ottenimento.")
#
#
# def fetch_reservations_for_accommodation_id(access_token_a, accommodation_id):
#     reservation_endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {access_token_a}"
#     }
#     response = requests.get(reservation_endpoint, headers=headers)
#
#     if response.status_code == 200:
#         reservations = response.json()
#         return reservations
#     else:
#         print(
#             f"Errore nell'ottenere le prime prenotazioni per l'alloggio {accommodation_id}, {headers}, {response.status_code}, {response.text}")
#         return []
#
#
# # Esempio di utilizzo:
# # Ottieni il token di accesso (già ottenuto precedentemente)
#
# # access_token_a = get_access_token2()
# # print(access_token_a)
# # Inserisci l'ID dell'alloggio per cui desideri ottenere le prenotazioni
# accommodation_id = "632966"
#
# # Ottieni le prenotazioni per l'alloggio selezionato utilizzando il token ottenuto
# reservations = fetch_reservations_for_accommodation_id(access_token_a, accommodation_id)
#
# # Controlla se ci sono prenotazioni
# if reservations:
#     print(f"{accommodation_id}: {reservations}")
#
#     # Converti le prenotazioni in formato JSON
#     reservations_json = json.dumps(reservations)
#
#     # Definisci l'URL del webhook al quale inviare le prenotazioni
#     webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
#
#     # Invia i dati al webhook
#     headers = {
#         "Content-Type": "application/json"
#     }
#
#     response = requests.post(webhook_url, data=reservations_json, headers=headers)
#
#     # Verifica la risposta del webhook
#     if response.status_code == 200:
#         print("Dati inviati con successo al webhook.")
#     else:
#         print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")
# else:
#     print("Nessuna prenotazione disponibile o errore nell'ottenimento.")
#
# print(f"{accommodation_id}:{reservations}")
#
#
#
# def fetch_webhooks(access_token_a):
#     endpoint = "https://api.octorate.com/connect/rest/v1/subscription"
#
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access_token_a}"
#     }
#
#     response = requests.get(endpoint, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
#         return []
#
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
       
# All'interno della funzione handle_custom_endpoint

# ...

# if tipo == 'RESERVATION_CREATED':
#     # Ricerca del contatto esistente prima di crearne uno nuovo
#     existing_contact = request.env['res.partner'].sudo().search([('email', '=', email_)], limit=1)
#     if existing_contact:
#         # Aggiornare il contatto esistente
#         existing_contact.write({
#             'name': guestsList_,
#             'street': address_,
#             'city': city_,
#             'phone': phone_
#         })
#         contact_id = existing_contact.id
#     else:
#         # Creazione di un nuovo contatto
#         contact_bb = request.env['res.partner'].sudo().create({
#             'company_type': 'person',
#             'name': guestsList_,
#             'street': address_,
#             'city': city_,
#             'email': email_,
#             'phone': phone_
#         })
#         contact_id = contact_bb.id

#     # Codice per la creazione della fattura e altre operazioni per una nuova prenotazione
#     # ...

# elif tipo == 'RESERVATION_CHANGE':
#     # Cerca la fattura esistente con il riferimento fornito
#     existing_invoice = request.env['account.move'].sudo().search([
#         ('refer', '=', refer_),
#         ('move_type', '=', 'out_invoice')
#     ], limit=1)

#     if existing_invoice:
#         # Aggiornamento della fattura esistente
#         existing_invoice.write({
#             # Aggiornamenti ai dettagli della fattura
#             # ...
#         })

#         # Aggiornamento del nome del cliente se cambiato
#         existing_contact = request.env['res.partner'].sudo().search([('id', '=', existing_invoice.partner_id.id)], limit=1)
#         if existing_contact and existing_contact.name != guestsList_:
#             existing_contact.write({'name': guestsList_})

#         # Aggiornamento delle linee di fattura
#         # ...

#     # Altri codici specifici per la gestione dei cambiamenti di prenotazione
#     # ...

# elif tipo == 'RESERVATION_CANCELLED':
#     # Gestione delle cancellazioni delle prenotazioni
#     # Trova la fattura corrispondente e aggiorna lo stato o esegui le azioni necessarie
#     # ...

# # Gestione di altri tipi di richieste o situazioni di errore
# # ...

# CONFRONTO TRA CODICI
# @http.route('/api/import', cors='*', auth='public', methods=['GET'], csrf=False, website=False)
#     def importazione(self, refresh_token=None, **post):

#         access_token = get_access_token(refresh_token)

#         if access_token:
#             print(f"Token di accesso ottenuto con successo: {access_token}")
#         else:
#             print("Errore nell'ottenere il token di accesso.")

#         url = "https://api.octorate.com/connect/rest/v1/reservation/872964?type=CHECKIN&startDate=2023-12-01"

#         # Header della richiesta con il token di autenticazione
#         headers = {
#             'accept': 'application/json',
#             'Authorization': f'Bearer {access_token}'
#         }

#         # Esegui la richiesta GET all'API
#         response = requests.get(url, headers=headers)

#         # Verifica se la richiesta ha avuto successo
#         if response.status_code == 200:
#             # Parsa la risposta JSON
#             data = response.json()

#             response_data_list = []

#             # Estrai le prenotazioni dalla lista "data" e cicla su di esse
#             for reservation in data.get("data", []):
#                 refer = reservation.get("refer")
#                 guests = reservation.get("guests", [])
#                 for guest in guests:
#                     # Ora puoi accedere ai campi dell'oggetto guest direttamente
#                     email = guest.get("email")
#                     familyName = guest.get("familyName")
#                     givenName = guest.get("givenName")
#                     phone = guest.get("phone")
#                     city = guest.get("city")
#                     nome_completo = str(givenName) + " " + str(familyName)
#                 pmsProduct = reservation.get("pmsProduct")
#                 totalGross = reservation.get("totalGross")
#                 channelName = reservation.get("channelName")
#                 paymentStatus = reservation.get("paymentStatus")
#                 paymentType = reservation.get("paymentType")
#                 roomGross = reservation.get("roomGross")
#                 totalGuest = reservation.get("totalGuest")
#                 checkin = reservation.get("checkin")
#                 checkout = reservation.get("checkout")
#                 createTime = reservation.get("createTime")
#                 channelNotes = reservation.get("channelNotes")
#                 roomName = reservation.get("roomName")

#                 checkin_date = fields.Date.from_string(checkin)
#                 checkout_date = fields.Date.from_string(checkout)
#                 data_creazione_mod = fields.Date.from_string(createTime)
#                 delta = checkout_date - checkin_date
#                 n_notti = delta.days
#                 quantity_soggiorno = totalGuest * n_notti


#                 # gestione della tipologia della camera
#                 # gestione della tipologia della camera
#                 pms_product_id = reservation.get("pmsProduct")
#                 dettagli_camera = fetch_room_cleaning_details(pms_product_id, refresh_token)
#                 stato_camera = dettagli_camera.get("clean")
#                 tipologia_camera = dettagli_camera.get("name")
#                 ultima_pulizia = dettagli_camera.get("lastCleaningDate")




#                 # Puoi fare ulteriori operazioni con i dati estratti per ogni prenotazione
#                 # Ad esempio, stampare i dati
#                 response_data = {
#                     "riferimento": refer,
#                     "speriamo romm groos": roomGross,
#                     "totalGuest": totalGuest,
#                     "checkin": checkin,
#                     "checkout": checkout,
#                     "createTime": createTime,
#                     "channelNotes": channelNotes,
#                     "email": email,
#                     "Nome Utente": nome_completo,
#                     "phone": phone,
#                     "city": city,
#                     "id comera": pmsProduct,
#                     "costo totale": totalGross,
#                     "Canale di prenotazione" : channelName,
#                     "Stato del pagamento": paymentStatus,
#                     "Tipo di pagamento": paymentType,
#                     "Nome stanza":  roomName,
#                     "Ultima pulizia": ultima_pulizia,
#                     "Tipologia camera": tipologia_camera,
#                     "Stato camera": stato_camera
#                 }

#                 response_data_list.append(response_data)


#                 team_vendite = request.env['crm.team'].sudo().search([('name', '=', channelName)], limit=1)
#                 if not team_vendite:
#                     team_vendite = request.env['crm.team'].sudo().create({'name': channelName})

#                 # Creazione della fattura
#                 room_booking_obj = []  # Inizializza la variabile come False
#                 customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
#                 customer_account = request.env['account.account'].sudo().search([('name', '=', 'Merci c/vendite')], limit=1)
#                 room_product = request.env['product.product'].sudo().search([('name', '=', roomName)], limit=1)
#                 if not room_product:
#                     room_product = request.env['product.product'].sudo().create({'name': roomName})
#                 tassa_soggiorno = request.env['product.product'].sudo().search([('name', '=', "Tassa soggiorno")], limit=1)


#             # ********CONTROLLO/CREAZIONE DEL CONTATTO******
#                 contact_bb = request.env['res.partner'].sudo().create({
#                     'company_type': 'person',
#                     'name': nome_completo,
#                     'city': city,
#                     'email': email,
#                     'phone': phone
#                 })

#                 # stampa l'ID del contatto appena creato
#                 contact_id = contact_bb.id
#                 intero_contact = int(contact_id)
#                 print("ID CONTATTO CREATO : ", intero_contact)

#                 room_booking_obj = request.env['account.move'].sudo().create({
#                     'state': 'draft',
#                     'journal_id': customer_invoice_journal.id,
#                     'refer': refer,
#                     'move_type': 'out_invoice',
#                     'checkin': checkin_date,
#                     'checkout': checkout_date,
#                     'totalGuest': totalGuest,
#                     'rooms': n_notti,
#                     'roomGross': roomGross,
#                     'partner_id': intero_contact,  # Utilizza l'ID del contatto come partner_id
#                     'invoice_date': checkin_date,
#                     # 'ref': room_name,
#                     'team_id': team_vendite.id,
#                     'email_utente': email,
#                     'telefono_utente': phone,
#                     'nome_stanza_utente': roomName,
#                     'nota_interna': channelNotes,
#                     'stato_del_pagamento': paymentStatus,
#                     'tipo_di_pagamento': paymentType,
#                     'pulizia_camera': stato_camera,
#                     'ultima_pulizia': ultima_pulizia,
#                     'tipologia_camera': tipologia_camera,

#                 })

#                 # Creazione delle linee della fattura
#                 linee_fattura = []

#                 # Linea per il prodotto 1 (Pernotto)
#                 linea_fattura_pernotto = {
#                     'move_id': room_booking_obj.id,
#                     'product_id': room_product.id,  # ID del prodotto 'Pernotto' nel portale amministrazione
#                     'name': f"Prenotazione {refer} dal {checkin_date} al {checkout_date}",
#                     'quantity': 1,
#                     'price_unit': roomGross,
#                     'account_id': customer_account.id
#                 }
#                 linee_fattura.append(linea_fattura_pernotto)

#                 # Linea per il prodotto 2 (Tassa di Soggiorno)
#                 linea_fattura_tassasoggiorno = {
#                     'move_id': room_booking_obj.id,
#                     'product_id': tassa_soggiorno.id,  # ID del prodotto 'Tassa di Soggiorno' nel portale amministrazione
#                     'name': "Tassa di soggiorno",
#                     'quantity': quantity_soggiorno,
#                     'account_id': customer_account.id
#                 }
#                 linee_fattura.append(linea_fattura_tassasoggiorno)
#                 for line in linee_fattura:
#                     request.env['account.move.line'].sudo().create(line)

#                 room_booking_obj.with_context(default_type='out_invoice').write({'state': 'draft'})
#                 room_booking_obj.message_post(
#                     body=f"<p><b><font size='4' face='Arial'>Riepilogo dei dati:</font></b><br>"
#                          f"Refer: {refer}<br>"
#                          f"Prezzo totale: {roomGross}<br>"
#                          f"Ospiti: {totalGuest}<br>"
#                          f"Checkin: {checkin}<br>"
#                          f"Checkout: {checkout}<br>"
#                          f"Numero notti: {n_notti}<br>"
#                          f"Quantity soggiorno: {quantity_soggiorno}<br>"
#                          f"Prezzo unitario: {roomGross}<br>"
#                          f"City utente: {city}<br>"
#                          f"Email: {email}<br>"
#                          f"Guests List: {nome_completo}<br>"
#                          f"Telefono: {phone}<br>"
#                          f"<span style='color:red; font-weight:bold;'>Note interne: {channelNotes}</span><br>"
#                          f"Nome stanza: {roomName}<br>"
#                          f"Nome camera: {tipologia_camera}<br>"
#                          f"Pulizia camera:{stato_camera}<br>"
#                          f"Ultima pulizia:{ultima_pulizia}<br>"
#                          f"Piattaforma di prenotazione: {channelName}<br>"
#                          f"Stato del pagamento: {paymentStatus} <br>"
#                          f"Tipo di pagamento: {paymentType} </pr>",
#                     message_type='comment'
#                 )

#             return Response(json.dumps(response_data_list), content_type='application/json', status=200)
#         else:
#             print("Errore nella richiesta API:", response.status_code)
#             # In caso di errore, puoi restituire una risposta di errore appropriata
#             return Response("Errore nella richiesta API", content_type='text/plain', status=response.status_code)

