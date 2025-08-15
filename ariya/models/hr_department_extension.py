# -*- coding: utf-8 -*-

from odoo import models, fields
class Department(models.Model):
    _inherit = 'hr.department'

    ref_key = fields.Char(string='Ref Key')
    parent_key = fields.Char(string='Parent Key')

    _sql_constraints = [
        ('unique_ref_key', 'UNIQUE(ref_key)', 'Ref Key must be unique!')
    ]