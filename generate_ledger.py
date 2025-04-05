import random
from datetime import datetime, timedelta

# Function to generate random dates within the range of 2025
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Date range for the random dates
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# Generating random transactions
transactions = []
for i in range(20):
    date = random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
    account_type = random.choice(["Expense", "Revenue", "Liability", "Assets", "Equity"])
    account_name = random.choice([
        "Art Supplies Expense", "Gadget Manufacturing Expense", "Salaries Expense",
        "Marketing Expense", "Revenue from Gadget Sales", "Art Installation Expenses",
        "Gadget Assembly Costs", "Packaging Expense", "Legal Fees Expense", "Equipment Rental Expense",
        "Inventory Purchase Expense", "Art Licensing Fees", "Employee Bonus Expense",
        "Facility Rent Expense", "Research & Development Expense", "Utility Expense",
        "Shipment Expense", "Equipment Depreciation Expense", "Bank Loan Repayment", "Sales Tax Payable"
    ])
    debit = random.uniform(1000, 5000) if account_type == "Expense" else 0.0
    credit = random.uniform(1000, 5000) if account_type != "Expense" else 0.0
    description = f"Transaction related to {account_name.lower()}."
    reference = f"REF{random.randint(20250000, 20259999)}-{i+1:03d}"
    
    transaction = {
        "date": date,
        "account_type": account_type,
        "account_name": account_name,
        "debit": round(debit, 2),
        "credit": round(credit, 2),
        "description": description,
        "reference": reference
    }
    transactions.append(transaction)

transactions
