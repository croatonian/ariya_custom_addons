# -*- coding: utf-8 -*-
from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)

class HrEmployeeCustom(models.Model):
    _inherit = 'hr.employee'
    
    trips_ids = fields.Many2many('ariya_trip_manager.trip', string='Trips', groups="hr.group_hr_user")
    on_trip_1c = fields.Boolean(string="Trip Status 1C", default=False, groups="hr.group_hr_user")

    def write(self, vals):
        _logger.info("Updating employee %s with vals: %s", self.ids, vals)
        return super().write(vals)