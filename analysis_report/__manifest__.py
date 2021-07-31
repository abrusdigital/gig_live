# -*- coding: utf-8 -*-

{
    'name': 'Analysis Report',
    'version': '0.1',
    'summary': """Analysis Report""",
    'description': 'Analysis Report',
    'category': 'Generic Modules/Human Resources',
    'author': 'Abrus Networks',
    'company': 'Abrus Networks',
    'website': "https://www.abrusnetworks.com",
    'depends': ['base','project','helpdesk','report_xlsx','industry_fsm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/analysis_wizard.xml',
        'views/analysis_report.xml',
        'reports/report.xml',
        ],
    'demo': [],
    # 'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}