from odoo import fields, models


class WbBranch(models.Model):
    _name = 'wb.branch'
    _description = 'Bank Branches'

    name = fields.Char("Branch Name", required=True)
    code = fields.Char("Branch Code", required=True)
    address = fields.Text("Address")
    bank_id = fields.Many2one('wb.bank', string="Bank", required=True)
    manager_id = fields.Many2one('res.users', string="Branch Manager")
    employee_ids = fields.Many2many('res.users', string="Employees")