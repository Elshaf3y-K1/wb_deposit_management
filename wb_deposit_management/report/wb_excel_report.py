import io
import xlsxwriter
from odoo import models


class BankTransactionExcelReport(models.AbstractModel):
    _name = 'report.wb_deposit_management.bank_transaction_excel'
    _description = 'Bank Transaction Excel Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, transactions):
        sheet = workbook.add_worksheet('Bank Transactions')
        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm'})

        headers = [
            'Transaction ID', 'Customer', 'Bank', 'Type',
            'Amount', 'Commission', 'Total', 'Date'
        ]

        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        for row, transaction in enumerate(transactions, start=1):
            sheet.write(row, 0, transaction.id)
            sheet.write(row, 1, transaction.name.name)
            sheet.write(row, 2, transaction.bank_id.name)
            sheet.write(row, 3, 'Deposit' if transaction.tran_state == 'deposit' else 'Withdrawal')
            sheet.write(row, 4, transaction.balance, money_format)
            sheet.write(row, 5, transaction.commission_amount, money_format)
            sheet.write(row, 6, transaction.total_amount, money_format)
            sheet.write(row, 7, transaction.create_date, date_format)

        for col in range(len(headers)):
            sheet.set_column(col, col, 20)