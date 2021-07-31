# -*- coding: utf-8 -*-
# from odoo import http


# class GigChecklist(http.Controller):
#     @http.route('/gig_checklist/gig_checklist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gig_checklist/gig_checklist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gig_checklist.listing', {
#             'root': '/gig_checklist/gig_checklist',
#             'objects': http.request.env['gig_checklist.gig_checklist'].search([]),
#         })

#     @http.route('/gig_checklist/gig_checklist/objects/<model("gig_checklist.gig_checklist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gig_checklist.object', {
#             'object': obj
#         })
