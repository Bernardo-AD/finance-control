from src.card import Card

class Month:
    def __init__(self, name):
        self.name = name
        self.income = 0
        self.limit = 0
        self.reserves = []
        self.subscriptions = []
        self.cards = []

    def set_income(self, amount):
        self.income = amount

    def set_limit(self, amount):
        self.limit = amount

    def add_reserve(self, description, amount):
        self.reserves.append({"description": description, "amount": amount})

    def add_subscription(self, description, amount):
        self.subscriptions.append({"description": description, "amount": amount})

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_total_reserves(self):
        return sum(r["amount"] for r in self.reserves)

    def get_total_subscriptions(self):
        return sum(s["amount"] for s in self.subscriptions)

    def get_total_expenses(self):
        return sum(c.get_total() for c in self.cards)

    def get_total_outgoing(self):
        return self.get_total_reserves() + self.get_total_subscriptions() + self.get_total_expenses()

    def get_balance(self):
        return self.income - self.get_total_outgoing()

    def check_limit(self):
        if self.limit <= 0:
            return None
        spent = self.get_total_outgoing()
        percent = (spent / self.limit) * 100
        if spent > self.limit:
            return ("danger", percent, spent - self.limit)
        elif percent >= 80:
            return ("warning", percent, self.limit - spent)
        return ("ok", percent, self.limit - spent)