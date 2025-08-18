# -*- coding: utf-8 -*-

from odoo import api, models, fields

class Trip(models.Model):
    _name = 'ariya_trip_manager.trip'
    _description = 'Trip'

    date_from = fields.Date(string= 'Start date', default=fields.Date.today(), required=True)
    date_to = fields.Date(string = 'End date')

    destination_ids = fields.Many2many('res.country.state', string="Куди вiдрядження:", required=True)
    comment = fields.Text(string='Коментар')
    employees_ids = fields.Many2many('hr.employee', string='Співробітники', required=True)
    reason_for_trip_id = fields.Many2one('ariya_trip_manager.reason_for_trip', string='Мета відрядження', required=True)
