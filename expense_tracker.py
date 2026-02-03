from transaction import Transaction
from datetime import date
from datetime import datetime
import calendar
from store import Store, Filter, CategoryAggregationFilter, TypeAggregationFilter
import helpers

class ExpenseTracker:
    def __init__(self, store: Store):
        """Manages transactions"""
        self.store = store

    def add_transaction(self, transaction: Transaction):
        """Adds a new transaction"""
        self.store.create_transactions(transaction)
    
    def remove_transaction(self, index: int):
        """Removes a transaction by index"""
        return self.store.delete_transaction(index)

    def print_transactions(self):
        """Prints all transactions"""
        for i in range(len(self.list_of_transaction)):
           print(f"{i+1}: {self.list_of_transaction[i]} ")
        
    def get_total_income(self, start: date, end: date):
        """Calculates total income for date range"""
        filter = Filter(type = "income", start_date = start, end_date = end)
        return self.store.get_transactions(filter)
    
    def get_total_expense(self, start: date, end: date):
        """Calculates total expenses for date range"""
        filter = Filter(type = "expense", start_date = start, end_date = end)
        return self.store.get_transactions(filter)

    def get_expenses_by_category(self, date_filter: date = None):
        """Groups total expenses by category optionally filtered by date"""
        first_day = date_filter.replace(day = 1)
        last_day_num = calendar.monthrange(date_filter.year, date_filter.month)[1]
        last_day = date_filter.replace(day = last_day_num, hour=23, minute=59, second=59)
        
        filter = CategoryAggregationFilter(type = "expense",start_date = first_day, end_date = last_day )
        return self.store.aggregate_by_category(filter)
     
    def get_monthly_summary(self, date_filter: date):
        """Gets summary for specific month"""

        first_day = date_filter.replace(day = 1)
        last_day_num = calendar.monthrange(date_filter.year, date_filter.month)[1]
        last_day = date_filter.replace(day = last_day_num, hour=23, minute=59, second=59)
        filter_map= self.store.aggregate_by_type(TypeAggregationFilter(
            start_date=first_day,
            end_date=last_day
        ))

        income = 0
        expense = 0
        if 'income' in filter_map:
            income = filter_map['income']
        if 'expense' in filter_map:
            expense = filter_map['expense']
        
        net_balance = income - expense
        net_balance_formatted = helpers.get_formatted_amount(net_balance)
        
        print(f"{date_filter.strftime('%B')} {date_filter.year} FINANCIAL SUMMARY\nTotal Income: {helpers.get_formatted_amount(income)}\nTotal Expense: {helpers.get_formatted_amount(expense)},\nNet Balance: {net_balance_formatted}")
