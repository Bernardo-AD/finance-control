from src.card import Card
from src.month import Month
from src.report import generate_report

# Configurando o mês
abril = Month("Abril/2026")
abril.set_income(2500)

# Reservas
abril.add_reserve("Investimento", 500)
abril.add_reserve("Passar o mês", 500)

# Nubank
nubank = Card("Nubank")
nubank.add_expense("Tim", 87)
nubank.add_expense("Meli+", 9)
nubank.add_expense("Resident Evil Requiem", 95, total=285, installments=3, current=1)
abril.add_card(nubank)

# Segundo cartão
outro = Card("Inter")
outro.add_expense("Spotify", 22)
outro.add_expense("Netflix", 45)
abril.add_card(outro)

# Relatório
generate_report(abril)