from odoo import models


class TransactionReport(models.AbstractModel):
    _name = 'report.wb_deposit_management.transaction_report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['wb.bank.transactions'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'wb.bank.transactions',
            'docs': docs,
        }