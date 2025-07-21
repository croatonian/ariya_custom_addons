from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    firstname = fields.Char("Ім'я")
    lastname = fields.Char("Прізвище")
    lastname2 = fields.Char("По батькові")