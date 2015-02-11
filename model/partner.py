# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
#
#
import datetime

from openerp.osv import osv
from openerp.osv import fields


class res_partner(osv.osv):
    """Inherits OpenERP's res.partner. Adds mi.Hair custom values

    """
    _inherit = "res.partner"
    _get_name = lambda *x: datetime.datetime.now().strftime("%m%d%y%s%f")

    def create(self, cr, user, vals, context={}):
        #self._check_vals(vals)
        return super(res_partner, self).create(cr, user, vals, context)
                                                         
    def write(self, cr, user, ids,  vals, context={}):
        #self._check_vals(vals)
        return super(res_partner, self).write(cr, user, ids, vals, context)

    _columns = {
        'mihair_userid': fields.char('mi.Hair User ID', size=10),
        'mihair_vendorid': fields.char('mi.Hair Vendor ID', size=10),

        'mihair_uuid': fields.char('mi.Hair UUID', size=32),
        # Address related info
        'is_address': fields.boolean('Is Address?'),
        'is_salon': fields.boolean('Is Salon?'),

        # mi.Hair info
        # just for the is salon domain?
        'wifi': fields.boolean('WiFi enabled?'),
        'online_scheduling': fields.boolean('Online Scheduling'),

        # m2m
        'salon_types': fields.many2many('mihair.salon_type',
                                        'mihair_salon_type_rel',
                                        'salon_types', 'id',
                                        'Salon Type'),

        'additional_services': fields.many2many('mihair.additional_services',
                                                'mihair_add_services_rel',
                                                'additional_services', 'id',
                                                'Salon Additional Services'),

        'cell_carriers': fields.many2many('mihair.cell_carriers',
                                          'mihair_cell_carriers_rel',
                                          'cell_carriers', 'id',
                                          'Salon Cell Carriers'),

    }

    _defaults = {
        'is_address': False,
        'is_salon': False,
    }

    _sql_constraints = [
        ('mihair_vendorid_unique', 'UNIQUE(mihair_vendorid)',
         'mi.Hair vendor id must be unique must be unique'),
        ('email_unique', 'UNIQUE(email)',
         'email must be unique. This email address is already taken')
    ]
