# -*- coding: UTF-8 -*-

from openerp.osv import osv
from openerp.osv import fields


class purchase_order(osv.osv):
    """Adds spree information to OpenERP products"""
    _inherit = "purchase.order"

    _columns = {
        'spree_order_id': fields.char('Spree Order id'),
        #'spree_order_line_id': fields.char('Spree Order Line id'),
        'spree_order_line_id': fields.one2many('purchase.order.spree',
                                               'po_id',
                                               'Order Lines'),
        #'spree_order_line_id': fields.many2many('purchase.order.spree',
        #                                        'po_type_rel',
        #                                        'order_spree',
        #                                        'id',
        #                                        'Order Lines'),

        # Billing Address
        'spree_billing_full_name': fields.char('Full Name'),
        'spree_billing_address1': fields.char('Address 1'),
        'spree_billing_address2': fields.char('Address 2'),
        'spree_billing_city': fields.char('City'),
        'spree_billing_state': fields.char('State'),
        'spree_billing_zip': fields.char('Zip Code'),
        'spree_billing_phone': fields.char('Phone'),

        # Shipping Address
        'spree_shipping_full_name': fields.char('Full Name'),
        'spree_shipping_address1': fields.char('Address 1'),
        'spree_shipping_address2': fields.char('Address 2'),
        'spree_shipping_city': fields.char('City'),
        'spree_shipping_state': fields.char('State'),
        'spree_shipping_zip': fields.char('Zip Code'),
        'spree_shipping_phone': fields.char('Phone'),

        # Vendor Site Info
        'cherrypy_id': fields.char('URL ID'),
        'cherrypy_status': fields.boolean('Order Line Status'),
        'mail_carrier': fields.char('Carrier'),
        'tracking_number': fields.char('Tracking Number'),
        'vendor_comments': fields.text('Vendor Comments')
    }

    _defaults = {
        'cherrypy_status': False,
    }


class po_spree_line(osv.osv):
    """Adds spree information to OpenERP products"""
    _name = 'purchase.order.spree'
    _description = "List of Spree order lines already processed"

    _columns = {
        'po_id': fields.many2one('purchase.order', 'Purchase Order'),
        'spree_order_line': fields.char('Spree Order Line'),
    }

    _sql_constraints = [
        ('spree_order_line', 'UNIQUE(spree_order_line)',
         'Spree Order Line Number must be unique'),
    ]
