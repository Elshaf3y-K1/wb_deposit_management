from odoo import models, fields, api


class RecurringTransaction(models.Model):
    _name = 'wb.recurring.transaction'
    _description = 'Recurring Transactions'

    name = fields.Char("Name", required=True)
    customer_id = fields.Many2one('res.partner', "Customer", required=True)
    amount = fields.Float("Amount", required=True)
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], "Frequency", default='monthly')
    next_execution = fields.Date("Next Execution")

    def execute_recurring_transaction(self):
        for record in self:
            self.env['wb.bank.transactions'].create({
                'name': record.customer_id.id,
                'balance': record.amount,
                'tran_state': 'deposit',
                'remarks': f'Recurring transaction: {record.name}'
            })
            if record.frequency == 'daily':
                record.next_execution = fields.Date.add(record.next_execution, days=1)
            elif record.frequency == 'weekly':
                record.next_execution = fields.Date.add(record.next_execution, days=7)
            elif record.frequency == 'monthly':
                record.next_execution = fields.Date.add(record.next_execution, months=1)
            elif record.frequency == 'yearly':
                record.next_execution = fields.Date.add(record.next_execution, years=1)