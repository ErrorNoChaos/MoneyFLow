import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont

class TransactionPage(QWidget):
    def __init__(self, parent, user, transaction_type):
        super().__init__()
        self.parent = parent
        self.user = user
        self.transaction_type = transaction_type
        self.df = pd.read_csv('database.csv')
        self.transactions_df = pd.read_csv('transactions.csv')
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title_text = 'Deposit Amount' if self.transaction_type == 'deposit' else 'Withdraw Amount'
        title = QLabel(title_text)
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        layout.addWidget(QLabel('Enter Amount:'))
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_input)
        
        btn_layout = QHBoxLayout()
        
        confirm_btn = QPushButton('Confirm')
        confirm_btn.clicked.connect(self.process_transaction)
        btn_layout.addWidget(confirm_btn)
        
        back_btn = QPushButton('Back')
        back_btn.clicked.connect(lambda: self.parent.show_dashboard(self.user))
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        self.setLayout(layout)
    
    def process_transaction(self):
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                QMessageBox.warning(self, 'Error', 'Amount must be positive')
                return
            
            if self.transaction_type == 'withdraw' and amount > self.user['balance']:
                QMessageBox.warning(self, 'Error', 'Insufficient balance')
                return
            
            idx = self.df[self.df['account_id'] == self.user['account_id']].index[0]
            
            if self.transaction_type == 'deposit':
                self.df.at[idx, 'balance'] += amount
                trans_type = 'Deposit'
            else:
                self.df.at[idx, 'balance'] -= amount
                trans_type = 'Withdrawal'
            
            self.df.to_csv('database.csv', index=False)
            self.log_transaction(self.user['account_id'], trans_type, amount, self.df.at[idx, 'balance'])
            self.user['balance'] = self.df.at[idx, 'balance']
            
            QMessageBox.information(self, 'Success', f'{trans_type} of ${amount:.2f} successful')
            self.parent.current_user = self.user
            self.parent.show_dashboard(self.user)
        
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid amount')
    
    def log_transaction(self, acc_id, trans_type, amount, balance_after):
        new_transaction = pd.DataFrame({
            'account_id': [acc_id],
            'transaction_type': [trans_type],
            'amount': [amount],
            'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'balance_after': [balance_after]
        })
        self.transactions_df = pd.concat([self.transactions_df, new_transaction], ignore_index=True)
        self.transactions_df.to_csv('transactions.csv', index=False)