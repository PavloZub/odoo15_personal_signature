# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import route


class Academy(http.Controller):
    @http.route('/academy/academy', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['academy.teachers']
        return http.request.render('academy.index', {
            # 'teachers': ["Dianna Padilla", "Joddy Caroll", "Lester Vaughn"],
            'teachers': Teachers.search([])
        })


    # @http.route('/academy/<name>/', auth='public', website=True)
    # def teacher(self, name):
    #     return '<h1>{}</h1>'.format(name)

    @http.route('/academy/<int:id>', auth='public', website=True)
    def teacher(self, id):
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)


    @http.route('/academy/<model("academy.teachers"):teacher>', auth='public', website=True)
    def teacher(self, teacher):
        # return '<h1>Teacher {}</h1>'.format(teacher.name)
        return http.request.render('academy.biography', {'person': teacher})


    @route(['/academy/book_checkout/<model("library.checkout"):doc>'], auth="user", website=True)
    def portal_my_project(self, doc=None, **kw):
        # return request.render("library_portal.book_checkout", {"doc": doc})
        return '{}'.format(doc.name)

#     @http.route('/academy/academy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('academy.listing', {
#             'root': '/academy/academy',
#             'objects': http.request.env['academy.academy'].search([]),
#         })

#     @http.route('/academy/academy/objects/<model("academy.academy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('academy.object', {
#             'object': obj
#         })
