# -*- coding: utf-8 -*-
{
    'name': "ariya",

    'summary': """Adding fields to models""",

    'description': """Adding fields to models""",

    'author': "Jman Dig",
    'website': "https://jman.pp.ua",
    'license': "LGPL-3",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'depends': ['hr', 'hr_holidays'],
    'depends': ['hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        # 'views/hr_leave_views.xml',
        # 'views/hr_multi_leave_views.xml',
        # 'security/ir.model.access.csv'
        #'security/groups.xml'
    ],
}