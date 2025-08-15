# -*- coding: utf-8 -*-

from odoo import models, fields
class Job(models.Model):
    _inherit = 'hr.job'

    ref_key = fields.Char(string='Ref Key')
    kp_code = fields.Char(string='Код КП')
    kp_name = fields.Char(string='Назва по КП')

    _sql_constraints = [
        ('unique_ref_key', 'UNIQUE(ref_key)', 'Ref Key must be unique!')
    ]