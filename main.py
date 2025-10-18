import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from login_page import LoginPage
from dashboard_page import DashboardPage
from transaction_page import TransactionPage
from history_page import HistoryPage
class BankingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MoneyFlow')
        self.setGeometry(100, 100, 500, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.current_user = None
        self.show_login()
    
    def show_login(self):
        self.clear_layout()
        self.login_page = LoginPage(self)
        self.layout.addWidget(self.login_page)
    
    def show_dashboard(self, user):
        self.clear_layout()
        self.current_user = user
        self.dashboard_page = DashboardPage(self, user)
        self.layout.addWidget(self.dashboard_page)
    
    def show_deposit(self):
        self.clear_layout()
        self.transaction_page = TransactionPage(self, self.current_user, 'deposit')
        self.layout.addWidget(self.transaction_page)
    
    def show_withdraw(self):
        self.clear_layout()
        self.transaction_page = TransactionPage(self, self.current_user, 'withdraw')
        self.layout.addWidget(self.transaction_page)
    
    def show_history(self):
        self.clear_layout()
        self.history_page = HistoryPage(self, self.current_user)
        self.layout.addWidget(self.history_page)
    
    
    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BankingApp()
    window.show()
    sys.exit(app.exec_())
      


