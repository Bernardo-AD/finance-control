import pytest
from src.card import Card
from src.month import Month

# Testes do Card
def test_card_add_expense():
    card = Card("Nubank")
    card.add_expense("Tim", 87)
    assert len(card.list_expenses()) == 1

def test_card_get_total():
    card = Card("Nubank")
    card.add_expense("Tim", 87)
    card.add_expense("Meli+", 9)
    assert card.get_total() == 96

def test_card_installment():
    card = Card("Nubank")
    card.add_expense("Resident Evil", 95, total=285, installments=3, current=1)
    expense = card.list_expenses()[0]
    assert expense["installments"] == 3
    assert expense["current"] == 1
    assert expense["amount"] == 95

# Testes do Month
def test_month_income():
    month = Month("Abril/2026")
    month.set_income(2500)
    assert month.income == 2500

def test_month_reserves():
    month = Month("Abril/2026")
    month.set_income(2500)
    month.add_reserve("Investimento", 500)
    month.add_reserve("Passar o mês", 500)
    assert month.get_total_reserves() == 1000

def test_month_balance():
    month = Month("Abril/2026")
    month.set_income(2500)
    month.add_reserve("Investimento", 500)
    nubank = Card("Nubank")
    nubank.add_expense("Tim", 87)
    month.add_card(nubank)
    assert month.get_balance() == 2500 - 500 - 87

def test_month_total_expenses():
    month = Month("Abril/2026")
    nubank = Card("Nubank")
    nubank.add_expense("Tim", 87)
    nubank.add_expense("Meli+", 9)
    month.add_card(nubank)
    assert month.get_total_expenses() == 96