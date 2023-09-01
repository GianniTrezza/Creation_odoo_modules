{
    'name': 'Accreditamento',
    'author': 'Giovanni Trezza',
    'category': 'Health',
    'depends': ['base'],
    'website': 'www.odoo_accreditamento.tech',
    'summary': 'Processo accreditamento (Strutture Sanitarie)', 
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/accreditation.xml',
        'views/struttura_sanitaria.xml',
        'views/tipologia_pratica.xml', 
        'views/menu.xml',
        'views/res_partner_views.xml'  
    ],  
    'installable': True,
    'application': True,
}


