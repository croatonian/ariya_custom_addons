# -*- coding: utf-8 -*-

from odoo import fields, models

class ReasonForTrip(models.Model):
    _name = "ariya_trip_manager.reason_for_trip"
    _description = "Мета відрядження"
    name = fields.Char(string = 'Назва')