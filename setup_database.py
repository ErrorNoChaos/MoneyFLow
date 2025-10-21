import mysql.connector
from mysql.connector import Error

def setup_database():
    """
    Creates database, tables, and inserts initial data
    Run this ONCE when setting up the app
    """
    try:
        # Connect to MySQL (without database first)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Root@123'  # CHANGE THIS!
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Step 1: Create database if not exists
            print("Creating database...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS banking_app")
            cursor.execute("USE banking_app")
            print("✓ Database 'banking_app' created/verified")
            
            # Step 2: Create accounts table
            print("\nCreating accounts table...")
            create_accounts_table = """
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INT PRIMARY KEY,
                account_holder VARCHAR(100) NOT NULL,
                account_type VARCHAR(20) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL DEFAULT 0,
                pin INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_accounts_table)
            print("✓ Accounts table created/verified")
            
            # Step 3: Create transactions table
            print("\nCreating transactions table...")
            create_transactions_table = """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT PRIMARY KEY AUTO_INCREMENT,
                account_id INT NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                balance_after DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            )
            """
            cursor.execute(create_transactions_table)
            print("✓ Transactions table created/verified")
            
            # Step 4: Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM accounts")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Step 5: Insert initial account data
                print("\nInserting initial account data...")
                insert_accounts = """
                INSERT INTO accounts (account_id, account_holder, account_type, balance, pin)
                VALUES
                (1001, 'John Doe', 'Savings', 5000, 1234),
                (1002, 'Jane Smith', 'Checking', 3500, 5678),
                (1003, 'Bob Wilson', 'Savings', 2000, 9012),
                (1004, 'Alice Johnson', 'Checking', 8500, 3456),
                (1005, 'Fahad Ahmed', 'Savings', 20000, 6969),
                (1006, 'Harsh Yadav', 'Savings', 25000, 6968),
                (1007, 'Himadri', 'Savings', 1010000, 5969),
                (1008, 'Badhon', 'Savings', 10004500, 4568),
                (1009, 'Thanooj', 'Savings', 8000, 2345),
                (1010, 'Fahmi', 'Savings', 9000, 3567),
                (1011, 'Syed', 'Savings', 20000, 2163)
                """
                cursor.execute(insert_accounts)
                connection.commit()
                print("✓ Initial accounts inserted (11 accounts)")
                
                # Step 6: Insert initial transaction data
                print("\nInserting initial transaction data...")
                insert_transactions = """
                INSERT INTO transactions (account_id, transaction_type, amount, timestamp, balance_after)
                VALUES
                (1001, 'Deposit', 1000.0, '2025-01-15 10:30:00', 6000),
                (1002, 'Withdrawal', 500.0, '2025-01-16 11:45:00', 3000),
                (1008, 'Deposit', 10000000.0, '2025-10-18 19:32:29', 10005000),
                (1008, 'Withdrawal', 500.0, '2025-10-18 19:33:18', 10004500),
                (1005, 'Deposit', 10000.0, '2025-10-18 20:05:05', 20000),
                (1007, 'Deposit', 1000000.0, '2025-10-19 12:39:25', 1010000)
                """
                cursor.execute(insert_transactions)
                connection.commit()
                print("✓ Initial transactions inserted (6 transactions)")
            else:
                print(f"\n✓ Database already has {count} accounts. Skipping data insertion.")
            
            print("\n" + "="*50)
            print("DATABASE SETUP COMPLETE!")
            print("="*50)
            print("\nYou can now run your banking app.")        
            cursor.close()
            connection.close()
    
    except Error as e:
        print(f"Error during setup: {e}")

if __name__ == "__main__":
    print("="*50)
    print("BANKING APP - DATABASE SETUP")
    print("="*50)
    setup_database()