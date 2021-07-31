from odoo import models, fields, api, _
from datetime import datetime

class WizardReport(models.TransientModel): 
    _name = 'analysis.wizard' 
    
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    customer_id = fields.Many2one('res.partner',string="Customer")
    area_id = fields.Many2one('customer.branch',string="Area/Zone")
    building_id = fields.Many2one('building.building',string="Building")
    
    def print_report(self):
        return self.env.ref('analysis_report.analysis_report_xls').report_action(self)
        