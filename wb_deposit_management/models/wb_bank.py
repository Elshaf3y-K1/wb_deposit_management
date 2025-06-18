from odoo import api, fields, models, _


class WbBank(models.Model):
    _name = "wb.bank"
    _description = "Bank Model"

    name = fields.Char("Bank Name", required=True)
    code = fields.Char("Code", default='/', required=True)
    balance = fields.Float("Balance", compute="_get_final_bank_balance")
    partner_id = fields.Many2one("res.partner", string="Address")
    transaction_count = fields.Integer("Transaction Count", compute="_compute_transaction_count")
    daily_reconciliation = fields.Boolean("Daily Reconciliation", default=False)
    last_reconciliation_date = fields.Date("Last Reconciliation Date")
    reconciliation_line_ids = fields.One2many('wb.reconciliation.line', 'bank_id', string="Reconciliation Lines")

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code("wb.bank")
        return super(WbBank, self).create(vals)

    def _get_final_bank_balance(self):
        tran_obj = self.env['wb.bank.transactions']
        for record in self:
            all_transactions = tran_obj.search([
                ('bank_id', '=', record.id),
                ('state', '=', 'done')
            ])
            all_deposit = sum(all_transactions.filtered(
                lambda lm: lm.tran_state == 'deposit').mapped("balance"))
            all_withdraw = sum(all_transactions.filtered(
                lambda lm: lm.tran_state == 'withdraw').mapped("balance"))
            record.balance = (all_deposit - all_withdraw) or 0.00

    def _compute_transaction_count(self):
        for bank in self:
            bank.transaction_count = self.env['wb.bank.transactions'].search_count([
                ('bank_id', '=', bank.id)
            ])

    def action_daily_reconciliation(self):
        for bank in self:
            unreconciled_transactions = self.env['wb.bank.transactions'].search([
                ('bank_id', '=', bank.id),
                ('state', '=', 'done'),
                ('reconciled', '=', False)
            ])

            total = 0
            for transaction in unreconciled_transactions:
                total += transaction.total_amount
                transaction.write({'reconciled': True})

            bank.write({
                'last_reconciliation_date': fields.Date.today(),
                'reconciliation_line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'amount': total,
                    'reference': f'Reconciliation {fields.Date.today()}'
                })]
            })

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Bank name must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'Bank code must be unique!')
    ]