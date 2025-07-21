from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ua_city_type = fields.Selection(related='city_id.ua_type')
    ua_hromada_id = fields.Many2one(comodel_name='res.ua.hromada', related='city_id.ua_hromada_id')
    ua_region_id = fields.Many2one(comodel_name='res.ua.region', compute="_compute_ua_region")
    ua_district_id = fields.Many2one(comodel_name='res.ua.district', domain="[('city_id', '=', city_id)]")
    country_is_ua = fields.Boolean(compute='_compute_country_is_ua', help='Technical field for domain.')

    @api.depends('country_id')
    def _compute_country_is_ua(self):
        for partner in self:
            partner.country_is_ua = partner.country_id == partner.env.ref('base.ua')

    @api.depends('ua_hromada_id')
    def _compute_ua_region(self):
        for partner in self:
            if partner.ua_hromada_id:
                partner.ua_region_id = partner.ua_hromada_id.region_id
            else:
                partner.ua_region_id = False
