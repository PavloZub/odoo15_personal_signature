# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import date, timedelta



class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'open academy courses'

    name = fields.Char(string='Name', required =True)
    title = fields.Char(required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'open_academy.session', 'course_id', string="Sessions")

    _sql_constraints = [('check_description_title', 'CHECK(title!=description)',
                         'description and title are with same name')]
    # _sql_constraints = [
    #     ('name_course_uniq', 'unique(name)', 'Course names must be unique !'),
    # ]

    def copy(self, default=None):
        default = {}
        # copied_count = self.search_count([('name', '=like', u"Copy of {}%".format(self.name))])
        copied_count = self.search_count([('name', '=like', _(u"Copy of ") + u"{}%".format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of ") + u"{}".format(self.name)
            # new_name = u"Copy of {}".format(self.name)
        else:
            new_name = _(u"Copy of ") + u"{} ({})".format(self.name, copied_count)
            # new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

class Session(models.Model):
    _name = 'open_academy.session'
    _description = "OpenAcademy Sessions"

    today = date.today()
    name = fields.Char(required=True)
    start_date = fields.Date(default=today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    course_id = fields.Many2one('open_academy.course', ondelete='cascade', string="Course", required=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor",
            domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    #taken_seats = fields.Float(string='процент of taken seats', compute='_compute_taken_seats', store=True,)
    taken_seats = fields.Float(string='процент of taken seats')

    active = fields.Boolean(default=True)
    end_date = fields.Date(string='End Date',store=True , compute='_compute_get_end_date')
    attendees_count = fields.Integer(string="Attendes count", compute='_get_attendees_count', store=True)
    color = fields.Integer()
    _sql_constraints = [
        ('name_session_uniq', 'unique(name)', 'Sessions names must be unique !'),
    ]

    def wizard_open(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'open_academy.wizard',
            'view_mode': 'form',
            'target': 'new'
        }

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    @api.depends('start_date','duration')
    def _compute_get_end_date(self):
        for record in self:
            if (record.start_date and record.duration):
                duration = timedelta(record.duration)
                record.end_date = record.start_date + duration
            else:
                continue

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_indtructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id:
                if record.instructor_id in record.attendee_ids:
                    raise exceptions.ValidationsError(_("A instructor can't be an attendee"))

    @api.depends('seats')
    def _compute_taken_seats(self):
        for record in self:
            pass
            # if record.seats:
            #     record.taken_seats = (len(record.attendee_ids) / record.seats) * 100.0
            # else:
            #     record.taken_seats = 0.0

    # @api.onchange('seats')
    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats(self):
        # _my_object = self.env['open_academy.session']
        for record in self:
            if record.seats:
                if (self.seats < len(self.attendee_ids)) | (self.seats < 0):
                    return {
                        'warning': {
                            'title': _("Warning seats:incorrect 'seats value'"),
                            'message': _("more participants than seats or seats less zero"),
                        }
                    }

                record.taken_seats = (len(record.attendee_ids) / record.seats) * 100.0
                # _my_object.write({'taken_seats': record.taken_seats})
            else:
                record.taken_seats = 0.0
                # _my_object.write({'taken_seats': record.taken_seats})

            # if (self.seats < len(self.attendee_ids)) | (self.seats < 0):
            #     return {
            #         'warning': {
            #             'title': _("Warning seats:incorrect 'seats value'"),
            #             'message': _("more participants than seats or seats less zero"),
            #         }
            #     }
