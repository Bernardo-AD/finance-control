class Card:
    def __init__(self, name):
        self.name = name
        self.expenses = []

    def add_expense(self, description, amount, total=None, installments=None, current=None):
        expense = {
            "description": description,
            "amount": amount,
            "total": total,
            "installments": installments,
            "current": current
        }
        self.expenses.append(expense)

    def get_total(self):
        return sum(e["amount"] for e in self.expenses)

    def list_expenses(self):
        return self.expenses