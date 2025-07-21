# Copyright © 2024 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/master/legal/licenses.html#odoo-apps).

# flake8: noqa: E501

{
    'name': 'Settlements of Ukraine',
    'version': '18.0.1.1.0',
    'category': 'Localization',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/blog/odoo/kodifikator-administrativno-teritorialnikh-odinits-ta-teritorii-teritorialnikh-gromad-v-odoo-43',
    'license': 'OPL-1',
    'summary': 'Settlements of Ukraine according to the codifier of administrative-territorial units and territories of territorial communities.',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/ZIF',
    'depends': [
        'l10n_ua_state',
        'base_import_helper',
        'base_address_extended',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/res_country_state_data.xml',
        'views/res_ua_views.xml',
        'views/res_city_views.xml',
        'views/res_partner_views.xml',
        'wizard/base_import_helper_views.xml',
        'data/ir_action_todo_data.xml',
    ],
    'demo': [
        'data/res_country_demo.xml',
    ],
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
