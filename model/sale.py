# -*- coding: UTF-8 -*-

from openerp.osv import osv
from openerp.osv import fields


class sale_order(osv.osv):
    """Adds spree information to OpenERP products"""
    _inherit = "sale.order"

    _columns = {
        'spree_order_id': fields.char('Spree Order id'),
        #'spree_order_line_id': fields.char('Spree Order Line id'),
        'spree_order_line_id': fields.one2many('sale.order.spree',
                                               'so_id',
                                               'Order Lines'),

    }

    _defaults = {
    }


class so_spree_line(osv.osv):
    """Adds spree information to OpenERP products"""
    _name = 'sale.order.spree'
    _description = "List of Spree order lines already processed"

    _columns = {
        'so_id': fields.many2one('sale.order', 'SO'),
        'spree_order_line': fields.char('Spree Order Line'),
    }

    _sql_constraints = [
        ('spree_order_line', 'UNIQUE(spree_order_line)',
         'Spree Order Line Number must be unique'),
    ]
