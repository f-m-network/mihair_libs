# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
#
#
from pyechos.api import EchoSign

from openerp.tools.translate import _

from openerp.osv import osv
from openerp.osv import fields


class crm_lead(osv.osv):
    _inherit = "crm.lead"
    _description = "adding fields to crm.lead"

    def print_contract(self, cr, uid, ids, context=None):
        """Button"""
        data = {}
        return self._print_report(cr, uid, ids, data, context=context)

    def _print_report(self, cr, uid, ids, data, context=None):
        return {'type': 'ir.actions.report.xml',
                'report_name': 'webkit.contract_report',
                'data': data}

    def _get_mrr(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for o in self.browse(cr, uid, ids):
            res[o.id] = o.tablet_qty * o.monthly_price
        return res

    def _get_arr(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for o in self.browse(cr, uid, ids):
            res[o.id] = o.get_mrr * 12
        return res

    def _get_tcv(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for o in self.browse(cr, uid, ids):
            res[o.id] = o.get_arr * 2
        return res

    def _get_payment_url(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        r = self.pool.get('mihair.cherrypy')
        q = [('enabled', '=', True)]
        r_ids = r.search(cr, uid, q)
        cherry_url = r.read(cr, uid, r_ids[0])

        for o in self.browse(cr, uid, ids):
            res[o.id] = '{}/{}'.format(cherry_url, o.id)
        return res

    _columns = {
        'tablet_qty': fields.integer('Number of Tablets Required'),
        'monthly_price': fields.float('Monthly Price Per Tablet'),
        # Functional fields
        'get_mrr': fields.function(_get_mrr, method=True,
                                   string='Monthly Recurring Revenue'),
        'get_arr': fields.function(_get_arr, method=True,
                                   string='Annual Recurring Revenue'),
        'get_tcv': fields.function(_get_tcv, method=True,
                                   string='Total Contract Value'),
        # echosign
        'document_id': fields.char(string="EchoSign Contract ID"),
        'signed_doc': fields.boolean(string="Signed Document?"),

        # Stripe Initial payment
        'initial_payment': fields.boolean(string="Initial Payment"),

        # subscription
        'contract_payment': fields.function(_get_payment_url, method=True,
                                            string='Payment URL')
    }

    _defaults = {
        # TODO: get this from different table
        'monthly_price': 0,
    }

    def _get_echosign_credentials(self, cr, user):
        """Get EchoSign API credentials

        """
        r = self.pool.get('mihair.echosign')
        q = [('enabled', '=', True)]
        r_ids = r.search(cr, user, q)
        return r.read(cr, user, r_ids[0])

    def _get_echosign_api(self, cr, user):
        echo_api = self._get_echosign_credentials(cr, user)
        return EchoSign(echo_api.get('api_key'),
                        echo_api.get('application_secret'),
                        echo_api.get('application_id'))

    def _get_echosign_api_key(self, cr, user):
        echosign = self._get_echosign_api(cr, user)
        return echosign.get_access_token()

    def _send_contract_agreement(self, email, cr, user, ids, context):
        """Send contract agreement"""
        # Get Local Contract
        from openerp import netsvc
        ir_actions_report = self.pool.get('ir.actions.report.xml')
        q = [('report_name', '=', 'webkit.contract_report')]
        matching_reports = ir_actions_report.search(cr, user, q)

        report = ir_actions_report.browse(cr, user, matching_reports[0])
        report_service = 'report.' + report.report_name
        service = netsvc.LocalService(report_service)
        result, format = service.create(
            cr, user, ids,
            {'model': 'oerp_mihair.contract_report'},
            context=context)

        echo_creds = self._get_echosign_credentials(cr, user)
        echosign = self._get_echosign_api(cr, user)
        access_token = self._get_echosign_api_key(cr, user)

        # Sending document using binary object
        transient_id = echosign.transient_document(
            access_token.get('accessToken'),
            binary_object=result
        )

        # Sending signature request
        agreement = echosign.send_agreement(
            transient_id,
            access_token.get('accessToken'),
            echo_creds.get('contract_subject'),
            echo_creds.get('contract_message'),
            email
        )
        return agreement.get('agreementId')

    def get_func(self, cr, user, vals, context={}):
        print '\n\nClick me!\n\n'
        return {}

    def create(self, cr, user, vals, context={}):
        #self._check_vals(vals)
        return super(crm_lead, self).create(cr, user, vals, context)

    def write(self, cr, user, ids,  vals, context={}):
        # Get opportunity object
        opportunity = self.browse(cr, user, ids)[0]

        if opportunity.stage_id.id == 6:
            if not opportunity.signed_doc and not vals.get('signed_doc'):
                if vals.get('stage_id') != 6:
                    msg = _("The document must be signed before changing "
                            "stages")
                    raise osv.except_osv(_('Error!'), msg)
            else:
                print 'Me actualizaron'

        ##
        # If the client has only payed but haven't signed, must only be on
        # "Waiting for e-signature" and newly created subscriptions in cherrypy
        # will go to the "waiting for e-sign" column. In other words, if
        # an opportunity gets into 'waiting for e-sign' or id 6, it can't
        # go out unless the signature has been made

        # If the client paid and signed, can only be in Won

        # If the client is entered through Odoo, a unique URL must be created
        # relating it with the payment

        # For New and Qualification: no payments and no signatures have been
        # registered

        # If I just arrive to 5, 6, 7 or 8, I must check that the opportunity
        # has a defined partner and that partner must have an email address
        if vals.get('stage_id') in [5, 6, 7, 8]:
            if not opportunity.partner_id:
                msg = _("You must set a customer to the opportunity in order "
                        "to continue")
                raise osv.except_osv(_('Error!'), msg)
            elif opportunity.partner_id and not opportunity.partner_id.email:
                msg = _("You must set an email address to the customer "
                        "in order to continue")
                raise osv.except_osv(_('Error!'), msg)

        # If everything is fine, send document as soon as I get to 6
        if vals.get('stage_id') == 6:
            # Send contract
            agreement_id = self._send_contract_agreement(
                opportunity.partner_id.email,
                cr, user,
                ids, context)
            # Save agreement to current opportunity
            d = {'document_id': agreement_id}
            opportunity.write(d)

        # If a document is signed and payed, it can only be won

        # If opportunity is set to close, add or reject data when pushing
        # to mihair
        if vals.get('stage_id') == 7:
            # Check for partners and Raise exception if
            # opportunity has no partner defined
            for o in self.browse(cr, user, ids):
                if not o.partner_id:
                    msg = _('Opportunity must have a customer defined!')
                    raise osv.except_osv(_('Error!'), msg)

        "================================================"

        for o in self.browse(cr, user, ids):
            # Everything is ready. Lets create Rails Subscription
            if vals.get('stage_id') == 7:
                from .. lib.rqst import post_api

                # get these from DB
                api_url = 'http://mihair.herokuapp.com/api'
                api_name = '/subscribers'
                token = '227d860c6af94bac7cd79beea2fa8cea3390a745fdcf1d4f'

                # Set JSON values to send
                data = {
                    "subscriber": {
                        "email": o.partner_id.email,
                        "password": "password", # Create random password
                        "first_name": o.partner_id.name,
                        "last_name": o.partner_id.name,
                        "phone": o.partner_id.phone
                    }
                }

                # Make sure the connection goes through, if not, raise excpt
                rst = post_api(api_url, api_name, token, data)
                print rst.status_code

                # Also, if the user is added, notify in odoo adding
                # uuid to partner
                # response: 201
                if rst.status_code == 201:
                    mihair_uuid = rst.json().get('subscriber').get('uuid')
                    values = {'mihair_uuid': mihair_uuid}
                    partner_id = o.partner_id.id
                    # cr, uid, ids,
                    partner = self.pool.get('res.partner').browse(cr, user,
                                                                  partner_id)
                    partner.write(values)

                # Make sure user is not already in other system (response: 422)
                if rst.status_code == 422:
                    msg = _('User account is already registered'
                            ' in mihair system.'
                            ' Please check Customer Information')
                    raise osv.except_osv(_('Error!'), msg)

                # Connect to system and ensure that the connection is made,
                # otherwise disable the option to mark opportunity as won
                # and raise OERP exception

        return super(crm_lead, self).write(cr, user, ids, vals, context)
