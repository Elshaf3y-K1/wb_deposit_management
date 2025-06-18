from odoo import http
from odoo.http import request, Response
import json


class CustomerAPI(http.Controller):

    @http.route('/api/customer/<int:customer_id>', auth='public', methods=['GET'])
    def get_customer(self, customer_id, **kw):
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if not customer.exists():
            return Response(json.dumps({'error': 'Customer not found'}), 404)

        return Response(json.dumps({
            'id': customer.id,
            'name': customer.name,
            'balance': customer.balance,
            'bank': customer.wb_bank_id.name,
            'email': customer.email
        }), content_type='application/json')

    @http.route('/api/transaction/create', auth='user', methods=['POST'], csrf=False, type='json')
    def create_transaction(self, **post):
        required_fields = ['customer_id', 'bank_id', 'amount', 'type']
        if not all(field in post for field in required_fields):
            return {'error': 'Missing data'}

        try:
            transaction = request.env['wb.bank.transactions'].create({
                'name': post['customer_id'],
                'bank_id': post['bank_id'],
                'balance': float(post['amount']),
                'tran_state': 'deposit' if post['type'] == 'deposit' else 'withdraw'
            })
            return {'success': True, 'transaction_id': transaction.id}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/auth/login', auth='none', methods=['POST'], csrf=False, type='json')
    def login(self, **post):
        db = post.get('db')
        login = post.get('login')
        password = post.get('password')

        try:
            request.session.authenticate(db, login, password)
            return {
                'success': True,
                'session_id': request.session.sid,
                'user_id': request.env.user.id,
                'partner_id': request.env.user.partner_id.id
            }
        except Exception as e:
            return {'error': 'Authentication failed', 'details': str(e)}

    @http.route('/api/transactions/<int:customer_id>', auth='public', methods=['GET'])
    def get_transactions(self, customer_id, **kw):
        transactions = request.env['wb.bank.transactions'].sudo().search([
            ('name', '=', customer_id)
        ])

        result = []
        for t in transactions:
            result.append({
                'id': t.id,
                'date': t.create_date.strftime('%Y-%m-%d %H:%M'),
                'type': 'deposit' if t.tran_state == 'deposit' else 'withdraw',
                'amount': t.balance,
                'commission': t.commission_amount,
                'total': t.total_amount,
                'status': 'completed' if t.state == 'done' else 'pending'
            })

        return Response(json.dumps(result), content_type='application/json')