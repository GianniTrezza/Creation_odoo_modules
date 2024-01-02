{
    'name': 'Infratel',
    'version': '1.0',
    'author': 'Simone',
    'description': ' Esercizio - Infratel',
    'depends': ['base','calendar','crm','product','account','sale','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_details_views.xml',
        'views/framework_agreement_views.xml',
        'views/request.xml',
        'views/sla_policy.xml',
        'views/project_request.xml',
        'views/product.xml',
        'views/diameter_torque.xml',
        'views/drawn.xml',
        'views/unit_measure.xml',
        'views/request_line.xml',
        'views/iru_duration.xml',
        'views/custom_invoice.xml',
        'views/custom_invoice_line.xml',
        'views/custom_sales.xml',
        'views/odv_line.xml',
        'views/custom_purchase.xml',
        'views/oda_line.xml',
        'views/menu_views.xml',
        'views/tab_request.xml',
        'views/sla_label_views.xml'
    ],
    'images': ['static/description/icon.png'],
    'application': True
 
}