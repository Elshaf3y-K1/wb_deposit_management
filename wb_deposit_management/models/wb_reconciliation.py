from odoo import fields, models


class WbReconciliationLine(models.Model):
    _name = 'wb.reconciliation.line'
    _description = 'Bank Reconciliation Lines'

    date = fields.Date("Date", required=True)
    amount = fields.Float("Amount", required=True)
    reference = fields.Char("Reference")
    bank_id = fields.Many2one('wb.bank', string="Bank", required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)