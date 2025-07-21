# Copyright © 2024 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/17.0/legal/licenses.html).

from odoo import fields, models


class ResUaDistrict(models.Model):
    _name = 'res.ua.district'
    _description = 'City districts of Ukraine'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    city_id = fields.Many2one(comodel_name='res.city', string='City')
