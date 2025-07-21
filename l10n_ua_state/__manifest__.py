# Copyright © 2020 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Regions of Ukraine',
    'version': '18.0.1.0.0',
    'category': 'Localization',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop/regions-of-ukraine-22',
    'license': 'LGPL-3',
    'summary': 'Adds the regions of Ukraine',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/qeu',
    'depends': [
        'base',
    ],
    'data': [
        'data/res_country_state_data.xml',
        'data/ir_filters_data.xml',
        'views/res_country_state_views.xml',
    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
