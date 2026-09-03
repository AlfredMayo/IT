from datetime import datetime
import os

TRANSACTIONS_FILE = "transactions.txt"

def log_transaction(account_number, transaction_type, amount):
    """Log a new transaction to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{account_number}|{timestamp}|{transaction_type}|{amount:.2f}\n"
    
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(line)

def view_history(account_number=None):
    """View transaction history — optionally filter by account number"""
    if not os.path.exists(TRANSACTIONS_FILE):
        return ["No transactions found."]
    
    lines = []
    with open(TRANSACTIONS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 4:
                acc_num, timestamp, trans_type, amount = parts
                if account_number is None or acc_num == account_number:
                    lines.append(f"Timestamp: {timestamp}")
                    lines.append(f"Transaction: {trans_type}")
                    lines.append(f"Amount: ₱{amount}")
                    lines.append("")
    return lines if lines else ["No transactions found."]