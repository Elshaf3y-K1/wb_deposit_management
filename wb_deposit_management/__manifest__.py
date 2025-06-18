{
    'name': 'Bank Deposit Management',
    'version': '1.0',
    'summary': 'Manage bank deposits and withdrawals',
    'description': """
        Comprehensive system for managing bank transactions including deposits, 
        withdrawals, reporting, and customer portal
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'category': 'Finance',
    'depends': [
        'base',
        'mail',
        'web',
        'portal',
        'website',
        'report_xlsx'
    ],
    'data': [
        # Security
        'security/group_view.xml',
        'security/ir.model.access.csv',

        # Data
        'data/sequence_data.xml',
        'data/email_templates.xml',

        # Models
        'models/wb_bank.py',
        'models/wb_customers.py',
        'models/wb_transactions.py',
        'models/wb_reconciliation.py',
        'models/wb_branch.py',
        'models/wb_security.py',
        'models/wb_recurring.py',
        'models/loyalty.py',

        # Views
        'views/wb_bank_view.xml',
        'views/wb_customer_view.xml',
        'views/wb_bank_transactions_view.xml',
        'views/wb_branch_view.xml',
        'views/wb_dashboard.xml',
        'views/portal_templates.xml',

        # Reports
        'report/wb_excel_report.py',
        'report/transaction_report.py',

        # Controllers
        'controllers/customer_api.py',
        'controllers/notification_api.py',
        'controllers/portal.py',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}