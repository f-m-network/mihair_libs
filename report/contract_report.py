# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
# QN Cove Corporation
#

import time
from report import report_sxw
from osv import osv
from osv import fields


class create_contract_report(osv.osv_memory):
    _name = 'oerp_mihair.contract_report'

    def print_contract(self, cr, uid, ids, context=None):
        """Button"""
        data = {
            'ids': ids,
        }
        return self._print_report(cr, uid, ids, data, context=context)

    def _print_report(self, cr, uid, ids, data, context=None):
        return {'type': 'ir.actions.report.xml',
                'report_name': 'webkit.contract_report',
                'data': data}
    _columns = {
        'name': fields.char('mi.Hair User ID', size=10),
    }


class contract_print(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(contract_print, self).__init__(cr, uid, name, context=context)

        self.cr = cr
        self.uid = uid
        self.name = name

        self.localcontext.update({
            'leads': self._leads,
            'version': 0.1,
        })

    def _leads(self, id):
        return self.pool.get('crm.lead').read(self.cr, self.uid, id, [])

report_sxw.report_sxw('report.webkit.contract_report',
                      'crm.lead',
                      'contract_report.mako',
                      parser=contract_print
                      )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
