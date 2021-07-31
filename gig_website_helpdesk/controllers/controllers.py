# -*- coding: utf-8 -*-
import json
from odoo import http, _
from odoo.http import request

class gigHelpDesk(http.Controller):
    @http.route(['/get/buldings'], type='http', auth="public", website=True)
    def getCity(self, area, **post):
        data = []
        if area:
            area_id = request.env['customer.branch'].sudo().browse(int(area))
            for area in area_id.bulding_ids:
                data.append({
                'id' : area.id,
                'name' : area.name,
                })
            values = {
            'building' : data,
            }
        else:
            values = {
            'building' : False,
            }
        return  json.JSONEncoder().encode(values)

