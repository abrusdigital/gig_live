# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning


class hrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    area_ids = fields.Many2many('customer.branch')

    @api.onchange('area_ids')
    def _getAreaItems(self):

        if self.user_id:
            self.user_id.emp_area_ids = self.area_ids
       



class resUsers(models.Model):
    _inherit = 'res.users'

    emp_area_ids = fields.Many2many('customer.branch')

   