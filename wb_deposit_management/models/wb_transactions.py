from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WbBankTransactions(models.Model):
    _name = "wb.bank.transactions"
    _description = "Bank Transactions"

    name = fields.Many2one("res.partner", string="Customer", required=True)
    bank_id = fields.Many2one("wb.bank", string="Bank", required=True,
                              default=lambda lm: lm.env.user.wb_bank_id.id)
    branch_id = fields.Many2one(
        'wb.branch',
        string="Branch",
        default=lambda self: self.env.user.branch_id.id
    )
    balance = fields.Float("Amount")
    remarks = fields.Char("Remarks")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             string="State", default='draft')
    tran_state = fields.Selection([('deposit', 'Deposit'), ('withdraw', 'Withdraw')],
                                  string="Transaction Type", default='deposit', required=True)
    commission_rate = fields.Float("Commission Rate (%)", default=2.0)
    commission_amount = fields.Float("Commission Amount", compute="_compute_commission", store=True)
    total_amount = fields.Float("Total Amount", compute="_compute_total", store=True)
    reconciled = fields.Boolean("Reconciled", default=False)
    recurring = fields.Boolean("Recurring Transaction")
    recurrence_interval = fields.Integer("Recurrence Interval (days)")
    next_execution_date = fields.Date("Next Execution Date")

    @api.depends('balance', 'commission_rate')
    def _compute_commission(self):
        for record in self:
            record.commission_amount = (record.balance * record.commission_rate) / 100

    @api.depends('balance', 'commission_amount')
    def _compute_total(self):
        for record in self:
            if record.tran_state == 'deposit':
                record.total_amount = record.balance - record.commission_amount
            else:
                record.total_amount = record.balance + record.commission_amount

    def transaction_done(self):
        for record in self:
            if record.tran_state == 'withdraw' and record.name.balance < record.balance:
                raise UserError(_("Insufficient balance for withdrawal"))

            if record.tran_state == 'withdraw':
                today_withdrawals = self.search_count([
                    ('name', '=', record.name.id),
                    ('tran_state', '=', 'withdraw'),
                    ('create_date', '>=', fields.Date.today()),
                    ('state', '=', 'done')
                ])
                if today_withdrawals > record.name.daily_withdrawal_limit:
                    raise UserError("Daily withdrawal limit exceeded")

            record.state = 'done'
            record.message_post(
                body=f"Transaction {record.tran_state} of {record.balance} processed",
                subject=f"Transaction {record.id} Completed"
            )

            template = self.env.ref('wb_deposit_management.email_template_transaction_done')
            template.send_mail(record.id, force_send=True)

            record.name.add_loyalty_reward(record.balance)