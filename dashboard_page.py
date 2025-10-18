import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DashboardPage(QWidget):
    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user
        self.init_ui()
        self.check_minimum_balance()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel(f'Welcome, {self.user["account_holder"]}')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f'Account ID: {self.user["account_id"]}'))
        info_layout.addWidget(QLabel(f'Account Type: {self.user["account_type"]}'))
        info_layout.addWidget(QLabel(f'Balance: ${self.user["balance"]:.2f}'))
        layout.addLayout(info_layout)
        
        btn_layout = QHBoxLayout()
        
        deposit_btn = QPushButton('Deposit')
        deposit_btn.clicked.connect(self.parent.show_deposit)
        btn_layout.addWidget(deposit_btn)
        
        withdraw_btn = QPushButton('Withdraw')
        withdraw_btn.clicked.connect(self.parent.show_withdraw)
        btn_layout.addWidget(withdraw_btn)
        
        history_btn = QPushButton('Transaction History')
        history_btn.clicked.connect(self.parent.show_history)
        btn_layout.addWidget(history_btn)
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.parent.show_login)
        btn_layout.addWidget(logout_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        self.setLayout(layout)
    
    def check_minimum_balance(self):
        if self.user['balance'] < 1000:
            QMessageBox.warning(self, 'Alert', 'Your balance is below $1000!')