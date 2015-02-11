# -*- coding: utf-8 -*-

{
    'name': "oerp_mihair",
    'category': "",
    'version': "1.0",
    'depends': ['product', 'crm', 'report_webkit', 'purchase'],
    'author': "Juan Hernandez",
    'description': """\

odoo - spree integration
===========================================

""",

    'data': [
        "view/partner_view.xml",
        "view/product_view.xml",
        "view/crm_view.xml",
        "view/mihair_view.xml",
        "view/purchase_order_view.xml",
        "view/sale_order_view.xml",
        "report/contract_report.xml",
    ],
}
