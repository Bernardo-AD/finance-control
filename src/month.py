from src.card import Card

class Month:
    def __init__(self, name):
        self.name = name
        self.income = 0
        self.reserves = []
        self.cards = []

    def set_income(self, amount):
        self.income = amount

    def add_reserve(self, description, amount):
        self.reserves.append({"description": description, "amount": amount})

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_total_reserves(self):
        return sum(r["amount"] for r in self.reserves)

    def get_total_expenses(self):
        return sum(c.get_total() for c in self.cards)

    def get_balance(self):
        return self.income - self.get_total_reserves() - self.get_total_expenses()