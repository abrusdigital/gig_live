# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import Warning,ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"
    is_customer = fields.Boolean(string="is customer")
    areas_count = fields.Integer(compute='_compute_areas_count', string='Areas Count')
    buildings_count = fields.Integer(compute='_compute_buildings_count', string='Areas Count')
    bulding_ids = fields.One2many('building.building', 'partner_id', string='Buildings', domain=[('active', '=', True)])
    area_ids = fields.One2many('customer.branch', 'partner_id', string='Areas', domain=[('active', '=', True)])
    def action_open_googlemaps(self):
        """
        This Button method is used to open a URL
        according fields values.
        @param self: The object pointer
        """
        for line in self:
            url = "http://maps.google.com/maps?oi=map&q="
            if line.name:
                street_s = re.sub(r'[^\w]', ' ', line.name)
                street_s = re.sub(' +', '+', street_s)
                url += street_s + '+'
            if line.street:
                street_s = re.sub(r'[^\w]', ' ', line.street)
                street_s = re.sub(' +', '+', street_s)
                url += street_s + '+'
#                 if line.street2:
#                     street_s = re.sub(r'[^\w]', ' ', line.street2)
#                     street_s = re.sub(' +', '+', street_s)
#                     url += street_s + '+'
            if line.city:
                street_s = re.sub(r'[^\w]', ' ', line.city)
                street_s = re.sub(' +', '+', street_s)
                url += street_s + '+'
            if line.state_id:
                street_s = re.sub(r'[^\w]', ' ', line.state_id.name)
                street_s = re.sub(' +', '+', street_s)
                url += street_s + '+'
            if line.country_id:
                street_s = re.sub(r'[^\w]', ' ', line.country_id.name)
                street_s = re.sub(' +', '+', street_s)
                url += street_s + '+'
            if line.zip:
                url += line.zip
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': url
        }
    
    def _compute_buildings_count(self):
        for rec in self:
            rec.buildings_count = 0
            building_ids = self.env['building.building'].search([
            ('partner_id', '=', rec.id)])
            if building_ids:
                rec.buildings_count =  len(building_ids)
    
    def _compute_areas_count(self):
        for rec in self:
            rec.areas_count = 0
            areas_ids = self.env['customer.branch'].search([
            ('partner_id', '=', rec.id)])
            if areas_ids:
                rec.areas_count =  len(areas_ids)
    
    def action_open_areas(self):
        context = {
            'default_partner_id': self.id,
        }
        domain = [('partner_id', '=', self.id)]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Areas',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'customer.branch',
            'domain': domain,
            'context': context,
        }
    
    def action_open_buildings(self):
        context = {
            'default_partner_id': self.id,
        }
        domain = [('partner_id', '=', self.id)]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Building Info',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'building.building',
            'domain': domain,
            'context': context,
        }


    @api.model
    def create(self,vals):
        result = super(ResPartner,self).create(vals)
        if 'parent_id' in vals and vals['parent_id']:
            user = result.create_user_login(vals)
        return result

    def create_user_login(self,vals):
        if 'email' in vals and vals['email']:
            user_obj = self.env['res.users']
            check_user = user_obj.sudo().search([('login', '=', vals['email'])])
            if not check_user:
                grp_id = self.env.ref("base.group_portal")
                grpidval = "in_group_" + str(grp_id.id)
                user = user_obj.sudo().create({'login' : vals['email'],'name' : vals['name'] if vals['name'] else vals['email'],grpidval : True,'partner_id':self.id})
                self.user_id = user
                # user.action_reset_password()
                return user
            else:
                raise Warning('Another user already exists in the system with the same login ...')
        else:
            raise Warning('email not exists')
        return False
                   
