# -*- coding: UTF-8 -*-

from openerp.osv import osv
from openerp.osv import fields


class mihair_api(osv.osv):
    _name = 'mihair.api'
    _description = "miHair Spree API Access"

    _columns = {
        'name': fields.char(string='Name/Description', 
                            size=256, required=True),
        'url': fields.char(string='url', required=True),
        'api_key': fields.char(string='API Key')
    }


def unique_activation(self, cr, uid, vals, fields={}):
    """Ensures only one activated record """
    # Is 'enabled' set to true?
    if vals.get('enabled'):
        # Check for activated records
        r = self.pool.get('mihair.echosign')
        q = [('enabled', '=', True)]
        r_ids = r.search(cr, uid, q)

        # If there're activated records, set them to False
        if r_ids:
            a = r.read(cr, uid, r_ids[0])
            a['enabled'] = False
            r.write(cr, uid, r_ids, a, {})


class mihair_echosign(osv.osv):
    _name = 'mihair.echosign'
    _description = "miHair EchoSign API Access"

    def create(self, cr, uid, vals, context={}):
        unique_activation(self, cr, uid, vals)
        return super(mihair_echosign, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context={}):
        unique_activation(self, cr, uid, vals)
        return super(mihair_echosign, self).write(cr, uid, ids, vals, context)

    _columns = {
        'name': fields.char(string='Name/Description',
                            size=256, required=True),
        'api_key': fields.char(string='API Key', required=True),
        'application_secret': fields.char(string='Application Secret',
                                          required=True),
        'application_id': fields.char(string='Application ID', required=True),
        'enabled': fields.boolean(string='Enabled API Key'),
        # Contract contents
        'contract_subject': fields.char(string="Contract Subject"),
        'contract_message': fields.text(string="Contract Message"),
    }

    _defaults = {
        'enabled': False,
    }


class mihair_cherrypy(osv.osv):
    _name = 'mihair.cherrypy'
    _description = 'mi.Hair Cherrypy Configuration'

    def create(self, cr, uid, vals, context={}):
        unique_activation(self, cr, uid, vals)
        return super(mihair_cherrypy, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context={}):
        unique_activation(self, cr, uid, vals)
        return super(mihair_cherrypy, self).write(cr, uid, ids, vals, context)

    _columns = {
        'url': fields.char(string='mi.Hair Cherrypy URL',
                           size=256, required=True),
        'enabled': fields.boolean(string='Enabled API Key'),
    }

    _defaults = {
        'enabled': False,
    }


class mihair_salon_type(osv.osv):
    _name = 'mihair.salon_type'
    _description = "mi.Hair Salon Type"

    _columns = {
        'name': fields.char(string='Salon Type',
                            size=256, required=True),
    }


class mihair_additional_services(osv.osv):
    _name = 'mihair.additional_services'
    _description = "mi.Hair Salon Additional Services"

    _columns = {
        'name': fields.char(string='Salon Additional Services',
                            size=256, required=True),
    }


class mihair_cell_carriers(osv.osv):
    _name = 'mihair.cell_carriers'
    _description = "mi.Hair Salon Cell Carriers"

    _columns = {
        'name': fields.char(string='Salon Type',
                            size=256, required=True),
    }

