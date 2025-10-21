import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from db_connection import get_connection,close_connection

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
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
        
        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, 'Error', 'Database connection failed')
            return
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE account_id = %s AND pin = %s"
        cursor.execute(query, (acc_id, pin))
        user = cursor.fetchone()
        
        cursor.close()
        close_connection(conn)
        
        if not user:
            QMessageBox.warning(self, 'Login Failed', 'Invalid account ID or PIN')
        else:
            self.parent.show_dashboard(user)