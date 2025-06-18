from odoo import api, fields, models, _


class WbPartner(models.Model):
    _inherit = "res.partner"

    wb_bank_id = fields.Many2one("wb.bank", string="Bank",
                                 default=lambda self: self.env.user.wb_bank_id.id)
    balance = fields.Float("Balance", compute="_get_final_bank_balance")
    daily_withdrawal_limit = fields.Float("Daily Withdrawal Limit", default=5000.0)
    identity_verified = fields.Boolean("Identity Verified")
    identity_document = fields.Binary("Identity Document")

    def _get_final_bank_balance(self):
        tran_obj = self.env["wb.bank.transactions"]
        for record in self:
            all_transactions = tran_obj.search([
                ('bank_id', '=', record.wb_bank_id.id),
                ('name', '=', record.id),
                ('state', '=', 'done')
            ])
            all_deposit = sum(all_transactions.filtered(
                lambda lm: lm.tran_state == 'deposit').mapped("balance"))
            all_withdraw = sum(all_transactions.filtered(
                lambda lm: lm.tran_state == 'withdraw').mapped("balance"))
            record.balance = (all_deposit - all_withdraw) or 0.00


class WBUser(models.Model):
    _inherit = "res.users"

    wb_bank_id = fields.Many2one("wb.bank", string="Bank")
    branch_id = fields.Many2one('wb.branch', string="Branch")
    enable_2fa = fields.Boolean("Enable Two-Factor Authentication")
    last_otp = fields.Char("Last OTP")
    otp_expiry = fields.Datetime("OTP Expiry")

    def send_otp(self):
        self.write({
            'last_otp': '123456',  # In real implementation, generate random code
            'otp_expiry': fields.Datetime.add(fields.Datetime.now(), minutes=5)
        })
        return True

    def verify_otp(self, otp):
        if self.otp_expiry < fields.Datetime.now():
            return {'error': 'OTP expired'}
        if self.last_otp == otp:
            return {'success': True}
        return {'error': 'Invalid OTP'}