# -*- coding: utf-8 -*-

{
    'name': "Mutli Customer Branch Management",
    'version': '14.0.1.0.0',
    'summary': """Easily create, manage, and track Customer Branches.""",
    'description': """Easily create, manage, and track Customer Branches.""",
    'category': 'Service Management',
    'author': 'abrusnetworks',
    'company': 'abrusnetworks',
    'maintainer': 'abrusnetworks',
    'website': "https://www.abrusnetworks.com",
    'depends': ['base','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_branch_view.xml',
        'views/building_view.xml',
        'views/res_partner_view.xml'
    ],
    'demo': [ ],
#     'images': ["static/description/banner.png"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
