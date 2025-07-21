# Copyright © 2024 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/17.0/legal/licenses.html).

import io
import logging
from typing import Dict, List
import urllib3

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.addons.base_import.models.base_import import load_workbook

_logger = logging.getLogger(__name__)


class ImportHelper(models.TransientModel):
    _inherit = 'base_import.helper'

    mode = fields.Selection(selection_add=[('ukraine_katotth', 'Ukraine Cities')], ondelete={'ukraine_katottg': 'set null'})

    @api.model
    # pylint: disable-msg=too-many-locals,too-many-statements
    def parse_ua_codification(self, xls_data) -> None:
        """ Parse the ukrainian territorial codifier to get cities and other territorial objects. """

        state_mapping = {state.code: state.id for state in self.env.ref('base.ua').state_ids}

        book = load_workbook(io.BytesIO(xls_data or b''), data_only=True)
        sheets = book.sheetnames
        sheet_name = sheets[0]
        sheet = book[sheet_name]

        # XLS sheet line structure:
        # [0] - (Char) Country State/Oblast code   - model "res.country.state" (without parsing, use l10n_ua_state)
        # [1] - (Char) Country Oblast Region code  - model "res.ua.region"
        # [2] - (Char) Country Hromada code        - model "res.ua.hromada"
        # [3] - (Char) City code                   - model "res.city"
        # [4] - (Char) City District/Rayon code    - model "res.ua.district"
        # [5] - (Char) Territorial object category - use for City in the "ua_type" field
        # [6] - (Char) Territorial object name

        region_rows = []
        hromada_rows = []
        cities_rows = []
        district_rows = []

        for index, row in enumerate(sheet.rows, 2):
            if row[5].value == 'P':
                region_rows.append(row)
            elif row[5].value == 'H':
                hromada_rows.append(row)
            elif row[5].value in ['M', 'X', 'C']:
                cities_rows.append(row)
            elif row[5].value == 'B':
                district_rows.append(row)

        Region = self.env['res.ua.region']
        region_mapping: Dict[str, int] = {reg.code: reg.id for reg in Region.search([])}
        regions_to_create: List[Dict] = []
        for line in region_rows:
            code = line[1].value
            region_vals = {
                'name': line[6].value,
                'code': code,
                'state_id': state_mapping.get(line[0].value),
            }
            # Update
            if self.do_rewrite and code in region_mapping:
                region = Region.browse(region_mapping.get(code))
                region.sudo().write(region_vals)
            # Create
            elif code not in region_mapping:
                regions_to_create.append(region_vals)
        Region.sudo().create(regions_to_create)
        region_mapping = {reg.code: reg.id for reg in Region.search([])}

        Hromada = self.env['res.ua.hromada']
        hromada_mapping: Dict[str, int] = {hr.code: hr.id for hr in Hromada.search([])}
        hromada_to_create: List[Dict] = []
        for line in hromada_rows:
            code = line[2].value
            hromada_vals = {
                'name': line[6].value,
                'code': code,
                'region_id': region_mapping.get(line[1].value),
            }
            # Update
            if self.do_rewrite and code in hromada_mapping:
                hromada = Hromada.browse(hromada_mapping.get(code))
                hromada.sudo().write(hromada_vals)
            # Create
            elif code not in hromada_mapping:
                hromada_to_create.append(hromada_vals)
        Hromada.sudo().create(hromada_to_create)
        hromada_mapping = {hr.code: hr.id for hr in Hromada.search([])}

        City = self.env['res.city']
        city_mapping: Dict[str, int] = {
            city.ua_code: city.id for city in City.search([('country_id', '=', self.env.ref('base.ua').id)])
        }
        cities_to_create: List[Dict] = []
        for line in cities_rows:
            code = line[3].value
            city_vals = {
                'country_id': self.env.ref('base.ua').id,
                'state_id': state_mapping.get(line[0].value),
                'ua_hromada_id': hromada_mapping.get(line[2].value),
                'ua_code': code,
                'ua_type': line[5].value,
                'name': line[6].value,
            }
            # Update
            if self.do_rewrite and code in city_mapping:
                city = City.browse(city_mapping.get(code))
                city.sudo().write(city_vals)
            # Create
            elif code not in city_mapping:
                cities_to_create.append(city_vals)
        City.sudo().create(cities_to_create)
        city_mapping = {
            city.ua_code: city.id for city in City.search([('country_id', '=', self.env.ref('base.ua').id)])
        }

        District = self.env['res.ua.district']
        district_mapping: Dict[str, int] = {dis.code: dis.id for dis in District.search([])}
        district_to_create: List[Dict] = []
        for line in district_rows:
            code = line[4].value
            district_vals = {
                'name': line[6].value,
                'code': code,
                'city_id': city_mapping.get(line[3].value),
            }
            # Update
            if self.do_rewrite and code in district_mapping:
                district = District.browse(district_mapping.get(code))
                district.sudo().write(district_vals)
            # Create
            elif code not in district_mapping:
                district_to_create.append(district_vals)
        District.sudo().create(district_to_create)

    def action_import(self):
        self.ensure_one()
        if self.mode != 'ukraine_katotth':
            return super(ImportHelper, self).action_import()

        if not self.url or not self.url.startswith('https://mtu.gov.ua/'):
            raise UserError(_("The codifier URL is incorrect. Please specify a proper URL."))

        urllib3.disable_warnings()
        response = self.open_url(url=self.url, mode='content', verify=False)

        if response.get('error'):
            raise UserError(_('Error opening URL: %(err)s', err=response['error']))

        self.parse_ua_codification(response['content'].content)
        return {
            'name': _('Cities'),
            'type': 'ir.actions.act_window',
            'res_model': 'res.city',
            'view_mode': 'list,form',
            'domain': [('country_id', '=', self.env.ref('base.ua').id)],
            'target': 'current',
        }
