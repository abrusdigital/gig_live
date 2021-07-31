# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'
    
    
    
    
    def material_req(self):
        for rec in self:
            material_requisiton = self.env['material.requisitions'].create({
                'task' : rec.name,
                'customer': rec.partner_id.id or '',
                'area':rec.area_id.id,
                'building':rec.building_id.id
            })

        return {
            'name': 'name',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': material_requisiton.id,
            'res_model': 'material.requisitions',
            'context': "{}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            }
            
class MaterialRequisitions(models.Model):
    _name = 'material.requisitions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Material Requisitions"
    
    def _get_user_login(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        return user.id
    
    signature=fields.Binary(string="Signature")
    request_line = fields.One2many('requisition.lines', 'req_line', string='Order Lines')
    related = fields.Many2one('project.task')
    task = fields.Char(string="Task")
    customer = fields.Many2one('res.partner',string="Customer")
    area = fields.Many2one('customer.branch',string="Area")
    building = fields.Many2one('building.building',string="Building")
    requisition_date = fields.Date(string="Requisition Date",default=datetime.today())
    requested_by = fields.Many2one('res.users', string='Requested By',
                              default=_get_user_login)
    requisitions_lines = fields.One2many('requisition.lines','req_line')
    reason_req = fields.Text(string="Reason for Requisition")
    name = fields.Char(string="Service Number", readonly=True, required=True, copy=False, default='New')
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('material.requisitions')
        return super(MaterialRequisitions, self).create(vals)
        
    def send_requisition_email(self):
        if not self.signature:
            raise ValidationError("Please Sign the requisition")
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('material_requisitions', 'email_template_requisition')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id =  False
        ctx = {
            'default_model': 'material.requisitions',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
            }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
class RequisitionsLines(models.Model):
    _name = 'requisition.lines'
    
    req_line = fields.Many2one('material.requisitions',string="Requi")
    material = fields.Char(string="Material")
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity")
   