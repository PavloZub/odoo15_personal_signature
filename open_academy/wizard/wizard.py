# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'open_academy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_session(self):
        return self.env['open_academy.session'].browse(self._context.get('active_id'))
    session_id = fields.Many2one('open_academy.session', string="Session", required=True, default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    def reg_attendees(self):
        print("reg_attendees")
        for session in self.session_id:
            session.attendee_ids |= self.attendee_ids
        # The rs1 | rs2 operation is a union set operation and results in a recordset with
        # all elements from both recordsets. This is a set-like operation and won't result in
        # duplicate elements.
        # self.session_id.attendee_ids = self.session_id.attendee_ids | self.attendee_ids
        #rs[0] and rs[-1] retrieve the first element and the last element, respectively.
        # self.session_id.attendee_ids = self.attendee_ids[0]
        # self.session_id.attendee_ids =  self.attendee_ids[-1]
        #
        #The rs1 & rs2 operation is an intersection set operation
        # and results in a recordset
        # with only the elements present in both recordsets.
        # self.session_id.attendee_ids = self.session_id.attendee_ids & self.attendee_ids

        # The  rs1 - rs2 operation is a difference set operation and results in a recordset
        # with the rs1 elements not present in rs2.
        # self.session_id.attendee_ids = self.session_id.attendee_ids - self.attendee_ids
        return {}