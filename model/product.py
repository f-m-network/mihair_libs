# -*- coding: UTF-8 -*-
import os
import urllib
import base64
import datetime

from openerp.osv import osv
from openerp.osv import fields


class product_product(osv.osv):
    """Adds spree information to OpenERP products"""
    _inherit = "product.product"
    _get_name = lambda *x: datetime.datetime.now().strftime("%m%d%y%s%f")

    _columns = {
        'mihair_product_id': fields.char('mi.Hair Prod ID'),
    }
    _sql_constraints = [
        ('mihair_productid_unique',
         'UNIQUE(mihair_product_id)',
         'mi.Hair product id must be unique must be unique')
    ]

