import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QFont

class HistoryPage(QWidget):
    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user
        self.transactions_df = pd.read_csv('transactions.csv')
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Transaction History')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        user_transactions = self.transactions_df[
            self.transactions_df['account_id'] == self.user['account_id']
        ]
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Date', 'Type', 'Amount', 'Balance', 'Account ID'])
        table.setRowCount(len(user_transactions))
        
        for row, (idx, trans) in enumerate(user_transactions.iterrows()):
            table.setItem(row, 0, QTableWidgetItem(trans['timestamp']))
            table.setItem(row, 1, QTableWidgetItem(trans['transaction_type']))
            table.setItem(row, 2, QTableWidgetItem(f"${trans['amount']:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"${trans['balance_after']:.2f}"))
            table.setItem(row, 4, QTableWidgetItem(str(int(trans['account_id']))))
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        back_btn = QPushButton('Back to Dashboard')
        back_btn.clicked.connect(lambda: self.parent.show_dashboard(self.user))
        layout.addWidget(back_btn)
        
        self.setLayout(layout)