from odoo import models, fields


class drawn(models.Model):
    _name = "plant.routes"
    _rec_name = "code_drawn"
    
    code_drawn = fields.Char(string="Codice Tratta")
    point_a = fields.Char(string="Punto A (Nome pozzetto)")
    point_b = fields.Char(string="Punto Z (Nome pozetto)")
    node_code = fields.Char(string="Codice nodo")
    route_length = fields.Char(string="Lunghezza tratta")
    board = fields.Char(string="Tavola")
    from_street = fields.Char(string="Da Via/Civico")
    to_street = fields.Char(string="A Via/Civico")
    note = fields.Char(string="Note")
    diametro_fibre = fields.Many2one('diameter.torque', string="Diametro/Fibre cedute")
    
    #request = smartbutton
    #order = smartbutton
    