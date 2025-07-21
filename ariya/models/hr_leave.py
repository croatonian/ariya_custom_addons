# -*- coding: utf-8 -*-

from odoo import models, fields, api
class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'

    reason = fields.Many2one('reason_for_leave', string="Мета вiдрядження:")
    location = fields.Many2many('res.country.state', string="Куди вiдрядження:")
    leave_type_name = fields.Char(related='holiday_status_id.name')
    employee_buh_id = fields.Integer(related='employee_id.buh_id')
    reason_name = fields.Char(related='reason.name')
    location_name = fields.Char(compute='_compute_location_name')


    @api.depends('location')
    def _compute_location_name(self):
        for record in self:
            if record.location:
                # Example: Join names of related records with a comma
                #record.location_name = ", ".join(record.location.mapped('name'))
                names = [name + " область" for name in record.location.mapped('name')]
                record.location_name = ", ".join(names)
            else:
                record.location_name = False



