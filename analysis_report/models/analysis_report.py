# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TicketInherit(models.Model):
    _inherit = "helpdesk.ticket"
    
class ProjectInherit(models.Model):
    _inherit = "project.task"
    
