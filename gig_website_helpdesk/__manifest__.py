# -*- coding: utf-8 -*-
{
    'name': "gig_website_helpdesk",

    'summary': """
        Add new features for help desk""",

    'description': """
       website help desk
    """,

    'author': "Abrus Networks India Pvt. Ltd.",
    'website': "http://www.abrusnetworks.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website','helpdesk','website_helpdesk_form','customer_branch','ms_query','industry_fsm','web','contacts','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/default_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
