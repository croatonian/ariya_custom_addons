# -*- coding: utf-8 -*-

from odoo import models, fields
class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'
    buh_id = fields.Integer(string="Табельний номер 1С: ", required=True, groups="hr.group_hr_user")
    ref_key = fields.Char(string='Ref Key', groups="hr.group_hr_user")

    _sql_constraints = [
        ('unique_ref_key', 'UNIQUE(ref_key)', 'Ref Key must be unique!')
    ]

# _sql_constraints = [
#         ('uniq_name', 'unique(your_field_name)', "You Entered data is already exists with this name. Please give data must be unique!"),
#     ]