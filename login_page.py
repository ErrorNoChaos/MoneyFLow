import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.df = pd.read_csv('database.csv')
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('MoneyFlow')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        layout.addWidget(QLabel('Account ID:'))
        self.account_id_input = QLineEdit()
        layout.addWidget(self.account_id_input)
        
        layout.addWidget(QLabel('PIN:'))
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pin_input)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.verify_login)
        layout.addWidget(login_btn)    
        layout.addStretch()
        self.setLayout(layout)
    
    def verify_login(self):
        try:
            acc_id = int(self.account_id_input.text())
            pin = int(self.pin_input.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid input format')
            return
        
        user = self.df[(self.df['account_id'] == acc_id) & (self.df['pin'] == pin)]
        
        if user.empty:
            QMessageBox.warning(self, 'Login Failed', 'Invalid account ID or PIN')
        else:
            user_data = user.iloc[0].to_dict()
            self.parent.show_dashboard(user_data)