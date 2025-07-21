# Copyright © 2024 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/17.0/legal/licenses.html).

from odoo import fields, models


class ResUaHromada(models.Model):
    _name = 'res.ua.hromada'
    _description = 'Territorial hromadas of Ukraine'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    region_id = fields.Many2one(comodel_name='res.ua.region', string='Region')
    state_id = fields.Many2one(related='region_id.state_id', string='State')
