# -*- coding: utf-8 -*-
{
    'name': "gig_checklist",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','helpdesk','gig_website_helpdesk','industry_fsm','project'],

    # always loaded
    'data': [
        'security/checklist_security.xml',
        'security/ir.model.access.csv',
        'views/checklist_masterdata_view.xml',
        'views/equipment_view.xml',
        'views/project_task_inherit_view.xml',
        'views/templates.xml',
        'data/email_templates.xml',
        'views/hr_employee.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
