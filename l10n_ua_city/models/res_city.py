# Copyright © 2024 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/17.0/legal/licenses.html).

from odoo import fields, models


class City(models.Model):
    _inherit = 'res.city'
    _rec_names_search = ['name', 'zipcode', 'ua_code']

    ua_code = fields.Char(string='UA Code')
    ua_type = fields.Selection(
        selection=[
            ('M', 'City'),
            ('C', 'Village'),
            ('X', 'Settlement'),
        ],
        string='Type',
    )
    ua_hromada_id = fields.Many2one(comodel_name='res.ua.hromada', string='Hromada')
