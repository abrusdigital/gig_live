# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning


TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
    ('4', 'Urgent'),
    ('5', 'Urgent'),
]
class helpDeskinherit(models.Model):
    _inherit = 'helpdesk.ticket'
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0')
    note = fields.Html()



    @api.model
    def create(self, vals_list):
        res =  super(helpDeskinherit,self).create(vals_list)
        res.email_to_helpdesk_admin()
        return res


    def email_to_helpdesk_admin(self):
        helpdesk_admins = self.env['res.users'].search([('groups_id', 'in', self.env.ref('helpdesk.group_helpdesk_manager').id)])
        if helpdesk_admins:
            email = ''
            for user in helpdesk_admins:
                email += user.login
                email += ','
            email = email[:-1]
            message_obj=self.env.ref("gig_checklist.new_admin_ticket_request_email_template")
            if message_obj:
                values = message_obj.sudo().generate_email(self.id,['email_to','subject','body_html'])
                values['email_to'] = str(email)
                values['subject'] = str(self.display_name)
                values['body_html'] = values['body_html'].replace("__id__",str(self.id))
                send_mail = self.env['mail.mail'].sudo().create(values)
                send_mail.send()
            
