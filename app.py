from datetime import datetime
from transaction import Transaction
from expense_tracker import ExpenseTracker
from command import Command, Handler
from store import MemoryStore
import helpers

store = MemoryStore()
exp_tracker = ExpenseTracker(store)

def add_transaction():
    """Adds a new transaction"""
    amount = float(input("How much do you want to add: "))
    description = input("Write a description: ").lower()
    category = input("Which category? Food & Dining / Transportation / Entertainment / Shopping / Utilities: ").lower()
    date_str = input("Enter the date and time, 'ex: 2023-06-28 13:35': ")
    Transaction_type = input("'Expense' or 'Income': ").lower()

    date_format = '%Y-%m-%d %H:%M'
    date_obj= datetime.strptime(date_str, date_format)
    tr = Transaction(amount, description, category, date_obj, Transaction_type)
    exp_tracker.add_transaction(tr)

def expense_monthly():
    """Gets expenses in specific month"""
    date_str = input("Enter specific month to query: 'ex: 2023-06' ")
    date_format = '%Y-%m'
    date_obj= datetime.strptime(date_str, date_format)
    exp_by_cat = exp_tracker.get_expenses_by_category(date_obj)
    for item in exp_by_cat:
        print(f"{item.category}  {helpers.get_formatted_amount(item.total_amount)}")

def expense_date_range():
    """Gets expenses in date range"""
    start = input("Enter the start date: 'ex: 2023-06': ")
    end = input("Enter the end date: 'ex: 2023-08': ")
    date_format = '%Y-%m'
    date_obj_start = datetime.strptime(start, date_format)
    date_obj_end = datetime.strptime(end, date_format)
    total_expense = exp_tracker.get_total_expense(date_obj_start, date_obj_end)
    print(f"Total expenses in range  {start} and {end} is:")
    for item in total_expense:
        print(f"{item.category}   {helpers.get_formatted_amount(item.amount)}")
  
def summary():
    """Gets a summary of transactions"""
    user_date = input("Enter the specific month for financial summary: 'ex: 2025-06': ")
    date_filter = datetime.strptime(user_date, '%Y-%m')
    exp_tracker.get_monthly_summary(date_filter)
    
def expense_category():
    """Gets total expenses by category"""
    user_input = input("Do you want to see the result in a specific month?y/n ").lower()
    if user_input == "y":
        user_date = input("Enter the date: 'ex: 2025-06':")
        date_filter = datetime.strptime(user_date, '%Y-%m')
        print("EXPENSES BY CATEGORY: ")
        by_category = exp_tracker.get_expenses_by_category(date_filter)
        for item in by_category:
            print(f"{item.category}    {helpers.get_formatted_amount(item.total_amount)}")
    else:
        by_category = exp_tracker.get_expenses_by_category(date_filter)
        for item in by_category:
            print(f"{item.category}     {helpers.get_formatted_amount(item.total_amount)}")

def top_expense():
    """Gets top expenses"""
    start = input("Enter the start date: 'ex: 2023-06': ")
    end = input("Enter the end date: 'ex: 2023-08': ")
    date_format = '%Y-%m'
    date_obj_start = datetime.strptime(start, date_format)
    date_obj_end = datetime.strptime(end, date_format)
    print("TOP 5 EXPENSES: ")
    sorted_tr = exp_tracker.get_total_expense(date_obj_start, date_obj_end)
    reversed_list = reversed(sorted_tr)
    for item in reversed_list:
        print(f"{item.description}    {helpers.get_formatted_amount(item.amount)}   ({item.category})")
 
cmd = Command()
cmd.register_handlers("add", [Handler(add_transaction, "Add a new transaction")])

handlers = []
handlers.append(Handler(expense_monthly, "get a monthly expenses"))
handlers.append(Handler(expense_date_range, "expenses in date range"))
handlers.append(Handler(summary, "get a monthly summary of total income/expense and net balance"))
handlers.append(Handler(expense_category, "get total expenses of each category"))
handlers.append(Handler(top_expense, "get top expenses by transaction"))

cmd.register_handlers("query", handlers)

while True:
    user_command = input(f"Enter a command: {' / '.join(cmd.list_command())}: ")
    cmd.run(user_command)
