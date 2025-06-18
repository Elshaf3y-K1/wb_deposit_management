from odoo import http
from odoo.http import request


class DepositPortal(http.Controller):

    @http.route('/my/deposit', auth='user', website=True)
    def deposit_portal_home(self, **kw):
        partner = request.env.user.partner_id
        transactions = request.env['wb.bank.transactions'].search([
            ('name', '=', partner.id)
        ], order='create_date desc', limit=10)

        return request.render('wb_deposit_management.portal_home', {
            'partner': partner,
            'transactions': transactions,
            'balance': partner.balance,
        })

    @http.route('/my/transactions', auth='user', website=True)
    def deposit_transactions(self, **kw):
        partner = request.env.user.partner_id
        transactions = request.env['wb.bank.transactions'].search([
            ('name', '=', partner.id)
        ])

        return request.render('wb_deposit_management.portal_transactions', {
            'transactions': transactions,
        })

    @http.route('/my/deposit/request', auth='user', website=True)
    def request_deposit(self, **kw):
        banks = request.env['wb.bank'].search([])
        return request.render('wb_deposit_management.request_deposit', {
            'banks': banks,
        })

    @http.route('/my/deposit/submit', auth='user', website=True, methods=['POST'])
    def submit_deposit(self, **post):
        if not all(key in post for key in ['bank_id', 'amount']):
            return request.redirect('/my/deposit/request?error=missing_data')

        try:
            transaction = request.env['wb.bank.transactions'].sudo().create({
                'name': request.env.user.partner_id.id,
                'bank_id': int(post['bank_id']),
                'balance': float(post['amount']),
                'tran_state': 'deposit',
                'state': 'draft',
                'remarks': 'Requested via customer portal'
            })

            transaction.message_post(
                body=f"New deposit request for {post['amount']} from customer portal",
                subject="New Deposit Request"
            )

            return request.redirect('/my/deposit?success=request_submitted')
        except Exception as e:
            return request.redirect(f'/my/deposit/request?error={str(e)}')

    @http.route('/my/profile', auth='user', website=True)
    def deposit_profile(self, **kw):
        return request.render('wb_deposit_management.portal_profile', {
            'partner': request.env.user.partner_id,
        })