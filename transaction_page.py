from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from db_connection import get_connection, close_connection

class TransactionPage(QWidget):
    def __init__(self, parent, user, transaction_type):
        super().__init__()
        self.parent = parent
        self.user = user
        self.transaction_type = transaction_type
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
            
            conn = get_connection()
            if not conn:
                QMessageBox.critical(self, 'Error', 'Database connection failed')
                return
            
            cursor = conn.cursor()
            
            # Calculate new balance
            if self.transaction_type == 'deposit':
                new_balance = float(self.user['balance']) + amount
                trans_type = 'Deposit'
            else:
                new_balance = float(self.user['balance']) - amount
                trans_type = 'Withdrawal'
            
            # Update balance
            query = "UPDATE accounts SET balance = %s WHERE account_id = %s"
            cursor.execute(query, (new_balance, self.user['account_id']))
            
            # Log transaction
            query = """
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.user['account_id'], trans_type, amount, new_balance))
            
            conn.commit()
            cursor.close()
            close_connection(conn)
            
            self.user['balance'] = new_balance
            self.parent.current_user = self.user
            
            QMessageBox.information(self, 'Success', f'{trans_type} of ${amount:.2f} successful')
            self.parent.show_dashboard(self.user)
        
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid amount')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Transaction failed: {str(e)}')