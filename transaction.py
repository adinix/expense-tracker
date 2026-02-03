import helpers

class Transaction:
    """Initializes a new transaction """
    def __init__(self, amount, description, category, date, transaction_type):
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date
        self.transaction_type = transaction_type

    def is_expense(self):
        """Check if transaction is an expense"""
        return self.transaction_type == "expense"
        
    def is_income(self):
        """Check if transaction is an income"""
        return self.transaction_type == "income"
    
    def get_formatted_amount(self):
        """Return amount with currency symbol"""
        return helpers.get_formatted_amount(self.amount)
    
    def __str__(self):
        """Return formatted transaction"""
        return f"{self.description}  - {self.get_formatted_amount()}  {self.category}  {self.date}"
