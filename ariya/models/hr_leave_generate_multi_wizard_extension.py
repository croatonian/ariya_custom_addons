# -*- coding: utf-8 -*-

from odoo import models, fields, api
class HrLeaveGenerateMultiWizard(models.TransientModel):
    _inherit = 'hr.leave.generate.multi.wizard'

    reason = fields.Many2one('reason_for_leave', string="Мета вiдрядження:")
    location = fields.Many2many('res.country.state', string="Куди вiдрядження:")
    leave_type_name = fields.Char(related='holiday_status_id.name')
    reason_name = fields.Char(related='reason.name')
    location_name = fields.Char(related='location.name')

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


    def _prepare_employees_holiday_values(self, employees, date_from_tz, date_to_tz):
        self.ensure_one()
        work_days_data = employees._get_work_days_data_batch(date_from_tz, date_to_tz)
        return [{
            'name': self.name,
            'holiday_status_id': self.holiday_status_id.id,
            'date_from': date_from_tz,
            'date_to': date_to_tz,
            'request_date_from': self.date_from,
            'request_date_to': self.date_to,
            'number_of_days': work_days_data[employee.id]['days'],
            'employee_id': employee.id,
            'state': 'validate',
            'reason': self.reason.id,
            'location': self.location,
        } for employee in employees if work_days_data[employee.id]['days']]
