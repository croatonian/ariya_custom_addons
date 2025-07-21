# -*- coding: utf-8 -*-

from odoo import models, fields
class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'
    buh_id = fields.Integer(string="Табельний номер 1С: ", required=True)


# _sql_constraints = [
#         ('uniq_name', 'unique(your_field_name)', "You Entered data is already exists with this name. Please give data must be unique!"),
#     ]