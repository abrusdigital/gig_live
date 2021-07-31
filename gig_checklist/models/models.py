# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning


class gigChecklistProduct(models.Model):
    _name = 'checklist.equipment'

    name = fields.Char()
    description = fields.Text()
    model = fields.Char()
    next_action_date = fields.Integer()
    maintenance_duration = fields.Integer()
    period = fields.Integer()
    serial_no = fields.Char()
    category_id = fields.Many2one('checklist.equipment.category')

class gigChecklistMasterData(models.Model):
    _name = 'checklist.master.data'

    name = fields.Char(required=True)
    model = fields.Char()
    serial_no = fields.Char()
    equipment_id = fields.Many2one('checklist.equipment')
    checklist_item_ids = fields.One2many('checklist.master.list','master_id' ,auto_join=True)
    
    @api.onchange('equipment_id')
    def _getModelAndSerialNo(self):
        self.model = self.equipment_id.model
        self.serial_no = self.equipment_id.serial_no
        

class gigChecklistEquiomentCategory(models.Model):
    _name = 'checklist.equipment.category'

    name = fields.Char()


class gigChecklistList(models.Model):
    _name = 'checklist.master.list'

    master_id =  fields.Many2one('checklist.master.data')
    name = fields.Char(required=True)
    sl_no = fields.Char()
    display_type = fields.Selection([('line_section', "Section"),('line_note', "Note")], default=False, help="Technical field for UX purpose.")


class gigCheckProductlistList(models.Model):
    _name = 'project.checklist.master.list'
    sl_no = fields.Char()
    project_id =  fields.Many2one('project.task')
    name = fields.Char(required=True,string="Description")
    remarks = fields.Char(string="Remarks")
    bool_y = fields.Boolean(string="Y")
    bool_n = fields.Boolean(string="N")
    bool_na = fields.Boolean(string="NA")
    display_type = fields.Selection([('line_section', "Section"),('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    @api.onchange('bool_y')
    def _onchange_boolean(self):
        if self.bool_y:
            self.bool_n = False
            self.bool_na = False
    @api.onchange('bool_n')
    def _onchange_booleann(self):
        if self.bool_n:
            self.bool_y = False
            self.bool_na =False

    @api.onchange('bool_na')
    def _onchange_booleanna(self):
        if self.bool_na:
            self.bool_y = False
            self.bool_n = False

class gigChecklistProjectTask(models.Model):
    _inherit = 'project.task'

    is_maintanance =  fields.Boolean(default=False)
    checklist_id = fields.Many2one('checklist.master.data')
    master_checklist_ids = fields.One2many('project.checklist.master.list' ,'project_id')
    checklist_progress = fields.Float(compute='_compute_progress_count',default=0.0)
    max_rate = fields.Integer(string='Maximum rate', default=100)
    delay_count = fields.Integer()
    task_parent_id = fields.Many2one('project.task')
    delay_unit = fields.Selection([('month', 'Month'),('year','Year')],default='month')
    is_schedule_created = fields.Boolean(default=False)


    @api.model
    def create(self, vals_list):
        res =  super(gigChecklistProjectTask,self).create(vals_list)
        if not res.is_schedule_created:
            res.email_to_project_admin()
        return res


    def email_to_project_admin(self):
        fsm_admins = self.env['res.users'].sudo().search([('groups_id', 'in', self.env.ref('industry_fsm.group_fsm_manager').id)])
        if fsm_admins:
            email = ''
            for user in fsm_admins:
                email += user.login
                email += ','
            email = email[:-1]
            message_obj=self.env.ref("gig_checklist.fsm_admin_request_email_template")
            if message_obj:
                values = message_obj.sudo().generate_email(self.id,['email_to','subject','body_html'])
                values['email_to'] = str(email)
                values['subject'] = str(self.display_name)
                values['body_html'] = values['body_html'].replace("__name__",str(self.name))
                send_mail = self.env['mail.mail'].sudo().create(values)
                send_mail.send()

    

    @api.depends('master_checklist_ids')
    def _compute_progress_count(self):
        for rec in self:
            total_len = self.env['project.checklist.master.list'].sudo().search_count([('project_id','=',rec.id),('display_type','!=','line_section')])
            rec.checklist_progress = total_len
            if total_len != 0:
                completed_checklist = self.env['project.checklist.master.list'].sudo().search_count([('project_id','=',rec.id),('bool_y','=',True)])
                rec.checklist_progress = (completed_checklist * 100) / total_len
            else:
                rec.checklist_progress = 0

    @api.onchange('checklist_id')
    def _getchecklistItems(self):
        check_id = self.checklist_id
        checklist = []
        for check in self.master_checklist_ids:
            check.unlink()
        self.checklist_id = check_id

        checklist_item_ids = self.env['checklist.master.list'].sudo().search([('master_id','=',self.checklist_id.id)])
        for rec in checklist_item_ids:
            checklist.append((0, 0, {'name':rec.name,'project_id' : self.id,'sl_no' : rec.sl_no,'display_type' : rec.display_type}))
        self.sudo().update({'master_checklist_ids': checklist})


    def create_schedule_tasks(self):
        if not self.delay_count :
            raise Warning('Select Interval Delays')
        if not self.delay_unit :
            raise Warning('Select Interval Type')
        ending_day_of_current_year = datetime.now().date().replace(month=12, day=31)
        schedule_days = []
        planned_date = self.planned_date_begin
        
        if self.delay_unit == 'month':
            current_month = self.planned_date_begin.month
            month_diff = int((12 - current_month)/self.delay_count)
            for date in range(month_diff):
                nxt_date = planned_date + relativedelta(months=+self.delay_count)
                planned_date = nxt_date
                schedule_days.append(nxt_date)

            self.generate_scheduled_task(schedule_days)

        if self.delay_unit == 'year':
            current_year = self.planned_date_begin.year
            for date in range(4):
                nxt_date = planned_date + relativedelta(years=+self.delay_count)
                planned_date = nxt_date
                schedule_days.append(nxt_date)

            self.generate_scheduled_task(schedule_days)

        self.is_schedule_created =True
          
        return

    def generate_scheduled_task(self,schedule_days):
        checklist = []
        checklist_item_ids = self.env['checklist.master.list'].sudo().search([('master_id','=',self.checklist_id.id)])
        for rec in checklist_item_ids:
            checklist.append((0, 0, {'name':rec.name,'project_id' : self.id,'sl_no' : rec.sl_no,'display_type' : rec.display_type}))

        for day in schedule_days:
            vals = {'name':self.name,
                    'task_parent_id':self.id,
                    'project_id':self.project_id.id,
                    'partner_id':self.partner_id.id,
                    'planned_date_begin':day,
                    'planned_date_end':day,
                    'is_maintanance' : True,
                    'checklist_id':self.checklist_id.id,
                    'user_id' : False,
                    'area_id' : self.area_id.id,
                    'building_id' : self.building_id.id,
                    'is_schedule_created' : True,
                    'worksheet_template_id' : self.worksheet_template_id.id}
            task = self.sudo().create(vals)
            task.sudo().update({'master_checklist_ids': checklist})