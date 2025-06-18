from odoo import http
from odoo.http import request, Response
import json


class NotificationAPI(http.Controller):

    @http.route('/api/balance/notify', auth='public', methods=['POST'], csrf=False, type='json')
    def balance_notification(self, **post):
        if 'customer_id' not in post:
            return {'error': 'Customer ID required'}

        customer = request.env['res.partner'].sudo().browse(post['customer_id'])
        if not customer.exists():
            return {'error': 'Customer not found'}

        return {
            'success': True,
            'message': f'Balance notification sent to {customer.name}',
            'balance': customer.balance
        }