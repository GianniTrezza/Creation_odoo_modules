# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

from odoo import http
from odoo.http import request


class ChatgptController(http.Controller):
    @http.route(['/chatgpt_form'], type='http', auth="public", csrf=False,
                website=True)
    def question_submit(self):
        return http.request.render('is_chatgpt_integration.connector')

class FatturazioneController(http.Controller):

    @http.route('/upload_csv', type='http', auth='user', csrf=False, methods=['POST'])
    def upload_csv(self, **kw):
        # Supponiamo che il file venga inviato con il nome "file"
        csv_file = kw.get('file')

        # Creare un'istanza del modello e chiamare il metodo button_import
        fatture_model = request.env['tabella.fatture'].sudo()
        try:
            # Puoi adattare il metodo button_import per accettare un file anziché usarne uno dal record, oppure creare un nuovo metodo
            fatture_model.button_import_from_file(csv_file)
            return {"status": "success", "message": "File elaborato correttamente!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
