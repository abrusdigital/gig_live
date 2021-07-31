# -*- coding: utf-8 -*-

{
    'name': 'Material Requisitions',
    'version': '0.1',
    'summary': """Material Requisitions""",
    'description': 'Material Requisitions',
    'category': 'Generic Modules/Human Resources',
    'author': 'Abrus Networks',
    'company': 'Abrus Networks',
    'website': "https://www.abrusnetworks.com",
    'depends': ['base','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_requisitions.xml',
        'views/sequence.xml',
        'report/report_template.xml',
        'data/email_template_data.xml',
        
        ],
    'demo': [],
    # 'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
