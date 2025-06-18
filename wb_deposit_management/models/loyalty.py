from odoo import models, fields, api


class LoyaltyProgram(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Integer("Loyalty Points", default=0, compute="_compute_loyalty_points")
    loyalty_level = fields.Char("Loyalty Level", compute="_compute_loyalty_level")

    @api.depends('transaction_ids')
    def _compute_loyalty_points(self):
        for partner in self:
            transactions = self.env['wb.bank.transactions'].search([
                ('name', '=', partner.id),
                ('state', '=', 'done')
            ])
            partner.loyalty_points = int(sum(transactions.mapped('balance')) // 100

    @api.depends('loyalty_points')
    def _compute_loyalty_level(self):
        for partner in self:
            points = partner.loyalty_points
            if points < 100:
                partner.loyalty_level = "Basic"
            elif points < 500:
                partner.loyalty_level = "Silver"
            elif points < 1000:
                partner.loyalty_level = "Gold"
            else:
                partner.loyalty_level = "Platinum"

    def add_loyalty_reward(self, amount):
        self.loyalty_points += int(amount) // 10
