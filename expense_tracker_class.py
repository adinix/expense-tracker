from transaction import Transaction
from datetime import date


class ReportItem:
    def __init__(self,category, total_amount):
        self.category = category
        self.total_amount = total_amount
        
class ExpenseTracker:
    def __init__(self):
        """Manages transactions"""
        self.list_of_transaction : list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        """Adds a new transaction"""
        self.list_of_transaction.append(transaction)
    
    def remove_transaction(self, index: int):
        """Removes a transaction by index"""
        self.list_of_transaction.pop(index)

    def print_transactions(self):
        """Prints all transactions"""
        for i in range(len(self.list_of_transaction)):
           print(f"{i+1}: {self.list_of_transaction[i]} ")
        
    def get_total_income(self, start: date, end: date):
        """Calculates total income for date range"""
        total_income = 0
        for i in range(len(self.list_of_transaction)):
            if self.list_of_transaction[i].is_income() :
                if start < self.list_of_transaction[i].date < end:
                    total_income += self.list_of_transaction[i].amount
        return total_income   
    
    def get_total_expense(self, start: date, end: date):
        """Calculates total expenses for date range"""
        total_expense = 0
        for i in range(len(self.list_of_transaction)):
            if self.list_of_transaction[i].is_expense():
                if start < self.list_of_transaction[i].date < end:
                    total_expense += self.list_of_transaction[i].amount
        return total_expense        
            
    
    def get_balance(self):
        """Gets current balance (income - expenses)"""
        total_expense = 0
        total_income = 0
        
        for i in range(len(self.list_of_transaction)):
            if self.list_of_transaction[i].is_expense():
                total_expense += self.list_of_transaction[i].amount
            if self.list_of_transaction[i].is_income():
                total_income += self.list_of_transaction[i].amount
        return total_income - total_expense
    

    def get_expenses_by_category(self, date_filter: date = None):
        """Groups total expenses by category optionally filtered by date"""
        dic = {}
        for i in range(len(self.list_of_transaction)):
            a = self.list_of_transaction[i].date
            if date_filter != None:
                if a.month == date_filter.month and a.year == date_filter.year:
                    if self.list_of_transaction[i].transaction_type == "expense":
                        if not self.list_of_transaction[i].category in dic:
                            dic[self.list_of_transaction[i].category] = self.list_of_transaction[i].amount
                        else:
                            dic[self.list_of_transaction[i].category] += self.list_of_transaction[i].amount
            
            else:
                 if self.list_of_transaction[i].transaction_type == "expense":
                    if not self.list_of_transaction[i].category in dic:
                            dic[self.list_of_transaction[i].category] = self.list_of_transaction[i].amount
                    else:
                        dic[self.list_of_transaction[i].category] += self.list_of_transaction[i].amount
        return self.get_sorted_categories(dic) 
    
    def get_sorted_categories(self,category_map: dict, limit: int = 6):
        """Converts a map of categories to a sorted list of categories"""
        list_report_objects = []
        for item in category_map:
           report_object = ReportItem(item, category_map.get(item))
           list_report_objects.append(report_object)
        list_object = self.sort_report_items(list_report_objects)
        return list_object [:limit]
    
    def sort_report_items(self, list_report_objects: list[ReportItem]):
        """Sorts a list of categories"""
        if len(list_report_objects) < 2:
                return list_report_objects
            
        else:
            less = []
            greater = []
            pivot = list_report_objects[0]
            for i in range(1, len(list_report_objects)):
                if list_report_objects[i].total_amount <= pivot.total_amount:
                    less.append(list_report_objects[i])
                else:
                    greater.append(list_report_objects[i])
            return self.sort_report_items(greater) + [pivot] + self.sort_report_items(less)   
          
    
    def print_monthly_summary(self, date_filter: date):
        """Gets summary for specific month"""
        total_income = 0
        total_expense = 0
        for i in range(len(self.list_of_transaction)):
                a = self.list_of_transaction[i].date
                if a.month == date_filter.month and a.year == date_filter.year:
                    if self.list_of_transaction[i].transaction_type == "income":
                        total_income += self.list_of_transaction[i].amount
                    else:
                        total_expense += self.list_of_transaction[i].amount
        net_balance = total_income - total_expense
        
        print(f"{date_filter.strftime('%B')} {date_filter.year} FINANCIAL SUMMARY\n{'-'*10}\n{'-'*10}\nTotal income:   ${total_income}\nTotal expense:   ${total_expense}\nNet Balance:   ${net_balance}")
                    

    def get_sorted_expense_transactions(self, date_filter: date = None, limit: int = 5):
        """Returns a list of expense transactions"""
        expense_transaction_list = []
        for i in range(len(self.list_of_transaction)):
            a = self.list_of_transaction[i].date
            if self.list_of_transaction[i].transaction_type == "expense":
                if date_filter != None:
                    if a.month == date_filter.month and a.year == date_filter.year:
                        expense_transaction_list.append(self.list_of_transaction[i])
                else:
                    expense_transaction_list.append(self.list_of_transaction[i])
        sorted_transactions = self.sort_transaction(expense_transaction_list)
        return sorted_transactions[:limit]


    def sort_transaction(self, expense_transaction_list: list[Transaction]):
        """Sorts a list of expense transactions"""
        if len(expense_transaction_list) < 2:
            return expense_transaction_list
        else:
            pivot = expense_transaction_list[0]
            less = []
            greater = []
            for i in range(1, len(expense_transaction_list)):
                    if expense_transaction_list[i].amount <= pivot.amount:
                        less.append(expense_transaction_list[i])
                    else:
                        greater.append(expense_transaction_list[i])
            return self.sort_transaction(greater) + [pivot] + self.sort_transaction(less)



    


    