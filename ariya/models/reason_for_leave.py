from odoo import fields, models

class ReasonForLeave(models.Model):
    _name = "reason_for_leave"
    _description = "Reason For Leave"

    name = fields.Char()