# -*- coding: utf-8 -*-
{
    'name': "ariya_trip_manager",

    'summary': """
        Business trip management module""",

    'description': """
        A module for the management of business trips with detail
        and tracking of every step.
    """,

    'author': "Jman Dig",
    'website': "https://jman.pp.ua",
    'license': "LGPL-3",

    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['base', 'hr', 'ariya', 'mail', "base_tier_validation"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/trip.xml',
        'views/tier_validation_templates_override.xml',
        'views/hr_employee_views.xml'
    ],
    'application' : True,

}
