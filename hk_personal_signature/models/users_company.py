# -*- coding: utf-8 -*-
from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    # Add a new column to the res.company model, by default partners are not
    # sign  image

    stamp_image = fields.Binary(string="Stamp of company")

class Users(models.Model):
    _inherit = 'res.users'

    # Add a new column to the res.company model, by default partners are not
    # sign and stamp image
    sign_image = fields.Binary(string="Personal signature")


