# -*- coding: utf-8 -*-
# from odoo import http


# class HrCustoizations(http.Controller):
#     @http.route('/hr_custoizations/hr_custoizations', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_custoizations/hr_custoizations/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_custoizations.listing', {
#             'root': '/hr_custoizations/hr_custoizations',
#             'objects': http.request.env['hr_custoizations.hr_custoizations'].search([]),
#         })

#     @http.route('/hr_custoizations/hr_custoizations/objects/<model("hr_custoizations.hr_custoizations"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_custoizations.object', {
#             'object': obj
#         })
