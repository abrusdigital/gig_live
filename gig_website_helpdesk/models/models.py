# -*- coding: utf-8 -*-
from odoo import models, fields, api


TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
    ('4', 'Urgent'),
    ('5', 'Urgent'),
]

class gigWebsite(models.Model):
	_inherit = "website"

	def get_areaZone(self):
		partner_id = self.env.user.partner_id
		partner_area = []
		area_ids = self.env['customer.branch'].sudo().search([])
		for area in area_ids:
			if partner_id.id in area.related_partners.ids:
				partner_area.append(area)
		return partner_area

class gigHelpdeskTicket(models.Model):
	_inherit = "helpdesk.ticket"
	area_id = fields.Many2one('customer.branch',string="Area/Zone")
	building_id = fields.Many2one('building.building',string="Building")
	tranfer_to = fields.Many2one('res.users', string='Transfer to',domain=lambda self: [('groups_id', 'in', self.env.ref('industry_fsm.group_fsm_manager').id)])

	# please execute this query to whitelist fields 
	# UPDATE ir_model_fields set website_form_blacklisted='false' WHERE model='helpdesk.ticket' AND name='building_id'
	# UPDATE ir_model_fields set website_form_blacklisted='false' WHERE model='helpdesk.ticket' AND name='area_id'
	
	@api.onchange('partner_id')
	def get_partner_area(self):
		self.area_id = False
		return {'domain':{'area_id':[('id','in',self.partner_id.area_ids.ids)]}}

	@api.onchange('area_id')
	def get_partner_buildings(self):
		self.building_id = False
		return {'domain':{'building_id':[('id','in',self.area_id.bulding_ids.ids)]}}


	def write(self, vals):
		res =  super(gigHelpdeskTicket, self).write(vals)
		if 'tranfer_to' in vals and vals['tranfer_to']:
			self.createFieldService()
			self.chage_ticket_state()
		return res

	def create(self, vals):
		res =  super(gigHelpdeskTicket, self).create(vals)
		if res.tranfer_to:
			res.createFieldService()
			res.chage_ticket_state()
		return res

	def createFieldService(self):
		task = self.env['project.task'].sudo().search([('task_id', '=' , self.id)])
		if task:
			task.write({'tranfer_to':self.tranfer_to.id})
		else:
			default_service = self.env['project.project'].sudo().search([('name', '=' , 'Field Service'),('company_id','=',self.env.user.company_id.id)],limit=1)
			default_worksheet = self.env['project.worksheet.template'].sudo().search([('name', '=' , 'Default Worksheet')],limit=1)
			pjt_task= self.env['project.task'].sudo().create({
			'name' : self.name,
			'tranfer_to':self.tranfer_to.id,
			'priority':self.priority,
			'description':self.note,
			'user_id' : False,
			'partner_id':self.partner_id.id,
			'project_id':default_service.id if default_service else False,
			'worksheet_template_id':default_worksheet.id if default_worksheet else False,
			'area_id':self.area_id.id if self.area_id else False,
			'building_id':self.building_id.id if self.building_id else False,
			'task_id':self.id})
	def chage_ticket_state(self):
		if self.stage_id.name == 'New':
			open_state_id = self.env['helpdesk.stage'].sudo().search([('name','=','Open')])
			self.stage_id = open_state_id.id

class HelpdeskProjectInherit(models.Model):
	_inherit = 'project.task'

	task_id = fields.Many2one('helpdesk.ticket')
	area_id = fields.Many2one('customer.branch',string="Area/Zone")
	building_id = fields.Many2one('building.building',string="Building")
	tranfer_to = fields.Many2one('res.users', string='Transfer to')
	priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0')

	

	@api.onchange('partner_id')
	def get_partner_area(self):
		self.area_id = False
		return {'domain':{'area_id':[('id','in',self.partner_id.area_ids.ids)]}}

	@api.onchange('area_id')
	def get_partner_buildings(self):
		self.building_id = False
		return {'domain':{'building_id':[('id','in',self.area_id.bulding_ids.ids)]}}


	def action_fsm_validate(self):
		result = super(HelpdeskProjectInherit, self).action_fsm_validate()
		if self.task_id:
			solved_state_id = self.env['helpdesk.stage'].sudo().search([('name','=','Solved')])
			self.task_id.stage_id = solved_state_id.id
		return result

	def action_open_building_googlemaps(self):
		return self.building_id.action_open_googlemaps()

	def write(self, vals):
		res =  super(HelpdeskProjectInherit, self).write(vals)
		if 'user_id' in vals and vals['user_id']:
			self.add_user_to_ticket()
			self.chage_ticket_state()
		return res

	def add_user_to_ticket(self):
		if self.task_id.stage_id.name == 'Open':
			self.task_id.user_id = self.user_id.id


	def chage_ticket_state(self):
		if self.task_id.stage_id.name == 'Open':
			inprogress_state_id = self.env['helpdesk.stage'].sudo().search([('name','=','In Progress')])
			self.task_id.stage_id = inprogress_state_id.id
	


    