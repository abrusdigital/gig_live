# -*- coding: utf-8 -*-
from odoo.exceptions import Warning
from odoo import models, fields, api, _
import re

class CustomerBranch(models.Model):
    _name = 'customer.branch'

    partner_id = fields.Many2one('res.partner', string='Related Customer', help="Customer", domain=[('active', '=', True)])
    name = fields.Char("Area Name")
    arabic_name = fields.Char("Arabic Name")
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    active = fields.Boolean("Active",default=True)
    contact_name = fields.Char("Contact Person")
    mobile = fields.Char("Contact Number")
    phone = fields.Char("Phone")
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    bulding_ids = fields.One2many('building.building', 'branch_id', string='Buildings', domain=[('active', '=', True)])
    buildings_count = fields.Integer(compute='_compute_buildings_count', string='Areas Count')
    related_partners = fields.Many2many('res.partner',string="Related Customers")
    area_related_contacts = fields.Char('Related Contact',compute='get_related_customers')

    def get_related_customers(self):
        for record in self:
            contacts = ''
            if record.related_partners:
                contacts = ''
                for rec in record.related_partners:               
                    contacts += rec.name + ','
                record.area_related_contacts = contacts[:-1]
            else:
                record.area_related_contacts = ''


    def name_get(self):
        res = super(CustomerBranch,self).name_get()
        result = []
        for area in self:
            if area.arabic_name:
                name = str(area.name) + "(" + str(area.arabic_name) + ")"
                result.append((area.id, name))
            else:
                name = str(area.name)
                result.append((area.id, name))
        return result

    def _compute_buildings_count(self):
        for rec in self:
            rec.buildings_count = 0
            building_ids = self.env['building.building'].search([
            ('branch_id', '=', rec.id)])
            if building_ids:
                rec.buildings_count =  len(building_ids)
    
    def action_open_buldings(self):
        context = {
            'default_branch_id': self.id,
            'default_partner_id': self.partner_id.id,
        }
        domain = [('branch_id', '=', self.id)]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Buildings',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'building.building',
            'domain': domain,
            'context': context,
        }


    def action_open_googlemaps(self):
        """
        This Button method is used to open a URL
        according fields values.
        @param self: The object pointer
        """
        if self.partner_id:
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

class BuilingBuilding(models.Model):
    _name = 'building.building'

    partner_id = fields.Many2one('res.partner', string='Related Customer', help="Customer")
    branch_id = fields.Many2one('customer.branch', string='Area', help="Area of the customer")
    name = fields.Char("Building Name")
    arabic_name = fields.Char("Arabic Name")
    floor = fields.Char("Floor No")
    room = fields.Char("Room No")
    contact_name = fields.Char("Contact Person")
    mobile = fields.Char("Contact Number")
    phone = fields.Char("Phone")
    active = fields.Boolean("Active",default=True)
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))

    
    def name_get(self):
        res = super(BuilingBuilding,self).name_get()
        result = []
        for area in self:
            if area.arabic_name:
                name = str(area.name) + "(" + str(area.arabic_name) + ")"
                result.append((area.id, name))
            else:
                name = str(area.name)
                result.append((area.id, name))
        return result
    
    def action_open_googlemaps(self):
        """
        This Button method is used to open a URL
        according fields values.
        @param self: The object pointer
        """
        if self.partner_id and self.branch_id:
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
    

