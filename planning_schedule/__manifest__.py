# -*- coding: utf-8 -*-

{
    'name': 'Planning Schedule',
    'version': '0.1',
    'summary': """Planning Schedule Views""",
    'description': 'Planning Schedule',
    'category': 'Generic Modules/Human Resources',
    'author': 'Abrus Networks',
    'company': 'Abrus Networks',
    'website': "https://www.abrusnetworks.com",
    'depends': ['base','project','gig_website_helpdesk'],
    'data': [
        #'security/ir.model.access.csv',
        'views/planning_schedule.xml',
        ],
    'demo': [],
    # 'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}