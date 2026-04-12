from transaction import Transaction

def generate_report(transaction: Transaction):
    print("==== RELATÓRIO FINANCEIRO ====")
    for t in transaction.list_all():
        symbol = "+" if t["type"] == "receita" else "-"
        print(f"{symbol} {t['description']}: R${t['amount']:.2f}")
    print ("--------------------------")
    print(f"Saldo final: R${transaction.get_balance():.2f}")