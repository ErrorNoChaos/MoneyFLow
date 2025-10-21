from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QFont
from db_connection import get_connection, close_connection

class HistoryPage(QWidget):
    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Transaction History')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        conn = get_connection()
        if not conn:
            layout.addWidget(QLabel('Database connection failed'))
            self.setLayout(layout)
            return
        
        cursor = conn.cursor()
        query = """
        SELECT transaction_id, transaction_type, amount, timestamp, balance_after
        FROM transactions
        WHERE account_id = %s
        ORDER BY timestamp DESC
        """
        cursor.execute(query, (self.user['account_id'],))
        user_transactions = cursor.fetchall()
        
        cursor.close()
        close_connection(conn)
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Date', 'Type', 'Amount', 'Balance', 'ID'])
        table.setRowCount(len(user_transactions))
        
        for row, trans in enumerate(user_transactions):
            trans_id, trans_type, amount, timestamp, balance_after = trans
            table.setItem(row, 0, QTableWidgetItem(str(timestamp)))
            table.setItem(row, 1, QTableWidgetItem(trans_type))
            table.setItem(row, 2, QTableWidgetItem(f"${amount:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"${balance_after:.2f}"))
            table.setItem(row, 4, QTableWidgetItem(str(trans_id)))
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        back_btn = QPushButton('Back to Dashboard')
        back_btn.clicked.connect(lambda: self.parent.show_dashboard(self.user))
        layout.addWidget(back_btn)
        
        self.setLayout(layout)