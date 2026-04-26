import json
import os

FILE = "data.json"

def save(months_data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(months_data, f, ensure_ascii=False, indent=2)

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def month_to_dict(month):
    return {
        "name": month.name,
        "income": month.income,
        "limit": month.limit,
        "reserves": month.reserves,
        "subscriptions": month.subscriptions,
        "cards": [
            {
                "name": card.name,
                "expenses": card.expenses
            }
            for card in month.cards
        ]
    }

def dict_to_month(data):
    from src.month import Month
    from src.card import Card
    month = Month(data["name"])
    month.set_income(data["income"])
    month.limit = data.get("limit", 0)
    month.reserves = data.get("reserves", [])
    month.subscriptions = data.get("subscriptions", [])
    for card_data in data.get("cards", []):
        card = Card(card_data["name"])
        card.expenses = card_data["expenses"]
        month.cards.append(card)
    return month